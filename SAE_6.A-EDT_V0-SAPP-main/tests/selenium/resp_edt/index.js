// tests/selenium/test_login.js
const { Builder, By, until, Select } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
const assert = require('assert');

const fs = require('fs');
const path = require('path');
    
async function runTestsInDirectory(directoryPath) {
    const files = fs.readdirSync(directoryPath);
    for (const file of files) {
        const filePath = path.join(directoryPath, file);
        if (path.extname(file) === '.js' && file !== 'index.js') {
            console.log(`Running tests in file: ${filePath}`);
            require(filePath);
        }
    }
}

runTestsInDirectory(path.join(__dirname));