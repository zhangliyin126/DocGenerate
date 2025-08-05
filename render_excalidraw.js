'use strict';

const fs = require('fs/promises');
const path = require('path');
const puppeteer = require('puppeteer');
const os = require('os');

// 将本地文件路径转换为浏览器可以访问的 file:// URL
function pathToFileURL(filePath) {
    let pathName = path.resolve(filePath).replace(/\\/g, '/');
    // Windows 驱动器号需要特殊处理
    if (pathName[0] !== '/') {
        pathName = '/' + pathName;
    }
    return 'file://' + pathName;
}

// 获取 excalidraw 库的绝对路径
const excalidrawScriptPath = require.resolve('@excalidraw/excalidraw/dist/excalidraw.production.min.js');
const excalidrawScriptURL = pathToFileURL(excalidrawScriptPath);

/**
 * 创建一个临时的HTML文件，该文件首先从CDN加载React和ReactDOM，
 * 然后再加载本地的Excalidraw库。这是成功的关键。
 * @returns {string} HTML content
 */
const createHtmlTemplate = () => `
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8" />
    <title>Excalidraw Renderer</title>
    <!-- 1. 先加载 React -->
    <script src="https://unpkg.com/react@17/umd/react.production.min.js" crossorigin></script>
    <!-- 2. 再加载 ReactDOM -->
    <script src="https://unpkg.com/react-dom@17/umd/react-dom.production.min.js" crossorigin></script>
</head>
<body>
    <div id="root"></div>
    <!-- 3. 最后加载 Excalidraw 库, 它会找到已经存在的 React 环境 -->
    <script type="text/javascript" src="${excalidrawScriptURL}"></script>
</body>
</html>
`;


async function renderInBrowser(inputFile, outputFile, tempDir) {
    let browser = null;
    const htmlPath = path.join(tempDir, 'render.html');

    try {
        const excalidrawContent = await fs.readFile(inputFile, 'utf-8');
        
        // 写入我们精心准备的HTML模板
        const htmlContent = createHtmlTemplate();
        await fs.writeFile(htmlPath, htmlContent);
        
        console.log('[INFO] Launching headless browser...');
        browser = await puppeteer.launch({
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });
        const page = await browser.newPage();
        await page.setDefaultNavigationTimeout(60000);
        
        page.on('console', msg => console.log(`[BROWSER LOG] ${msg.text()}`));
        page.on('pageerror', err => console.error(`[BROWSER ERROR] ${err.toString()}`));

        // 导航到本地HTML文件，确保所有脚本都加载完毕
        await page.goto(pathToFileURL(htmlPath), { waitUntil: 'networkidle0' });

        // 现在 ExcalidrawLib 和它的所有功能都已准备就绪
        const svgHTML = await page.evaluate(async (content) => {
            // 在浏览器上下文中进行最后的try-catch，以便获得更清晰的错误
            try {
                const { elements, appState } = JSON.parse(content);

                if (!elements || elements.length === 0) {
                    return { svg: '<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10"></svg>' };
                }

                const svg = await window.ExcalidrawLib.exportToSvg({
                    elements,
                    appState: {
                        ...appState,
                        exportWithPadding: true,
                        exportPadding: 10,
                        theme: 'light',
                    },
                    files: null,
                    getFont: async ({ family }) => {
                        const fontUrl = 'https://excalidraw.com/Virgil.woff2';
                        const response = await fetch(fontUrl);
                        if (!response.ok) throw new Error(`Failed to fetch font: ${response.statusText}`);
                        return response.arrayBuffer();
                    }
                });
                return { svg: svg.outerHTML };
            } catch (e) {
                // 如果在浏览器端出错，将错误信息包装后返回给Node.js
                return { error: e.message, stack: e.stack };
            }
        }, excalidrawContent);

        // 检查从浏览器返回的结果
        if (svgHTML.error) {
            console.error('[BROWSER EVALUATE ERROR]', svgHTML.error);
            console.error(svgHTML.stack);
            throw new Error('An error occurred inside the browser context.');
        }

        await fs.writeFile(outputFile, svgHTML.svg);
        console.log(`[SUCCESS] Successfully rendered SVG to ${outputFile}`);

    } catch (error) {
        console.error('[ERROR] An error occurred during Excalidraw rendering:', error);
        process.exit(1);
    } finally {
        if (browser) {
            console.log('[INFO] Closing headless browser.');
            await browser.close();
        }
        try { await fs.unlink(htmlPath); } catch (e) {}
    }
}


async function main() {
    const args = process.argv.slice(2);
    if (args.length !== 2) {
        console.error('Usage: node render_excalidraw.js <input_path> <output_path>');
        process.exit(1);
    }

    const [inputFile, outputFile] = args;
    const tempDir = path.dirname(outputFile);

    console.log(`[INFO] Input file: ${inputFile}`);
    console.log(`[INFO] Output file: ${outputFile}`);
    
    await renderInBrowser(inputFile, outputFile, tempDir);
}

main();