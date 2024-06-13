// tests/selenium/test_login.js
const { Builder, By, until, Select } = require("selenium-webdriver");
const chrome = require("selenium-webdriver/chrome");
const assert = require("assert");

async function selectFirst(driver, xpath) {
  let selectElement = await driver.wait(
    until.elementLocated(By.xpath(xpath)),
    10000
  );
  // await selectElement.click();
  let options = await selectElement.findElements(By.tagName("option"));
  for (let option of options) {
    let isDisabled = await option.getAttribute("disabled");
    if (!isDisabled) {
      // console.log(`Selecting option: ${await option.getText()}`);
      await option.click();
      return;
    }
  }
  throw new Error("No enabled options found in select element");
}

describe("Teacher Manager Test", function () {
  this.timeout(30000); // Increase timeout to handle network delays
  let driver;

  before(async function () {
    let options = new chrome.Options();
    // options.addArguments('headless'); // Run in headless mode
    driver = await new Builder()
      .forBrowser("chrome")
      .setChromeOptions(options)
      .build();
    await driver.manage().window().setRect({ width: 1920, height: 1080 });
  });

  after(async function () {
    await driver.quit();
  });

  it("login step", async function () {
    await driver.get("http://localhost:8180/login");
    await driver.findElement(By.id("username")).sendKeys("pbonnot1");
    await driver
      .findElement(By.xpath('//*[@id="form"]/div[2]/input'))
      .sendKeys("bonnot1234");
    await driver.findElement(By.xpath('//*[@id="form"]/button')).click();
    // await driver.wait(until.urlIs('http://localhost:4200/dashboard'), 5000);
    // let currentUrl = await driver.getCurrentUrl();
    await driver.wait(until.urlIs("http://localhost:8180/"), 5000);
    await driver.findElement(By.css('div[role="alert"]')).click();

    let token = await driver.executeScript(
      "return localStorage.getItem('auth-token');"
    );

    assert.ok(token, "Token should be stored in localStorage");
  });

  it("add teacher step", async function () {
    await driver
      .findElement(By.xpath('//*[@id="cal-date-nav-buttons"]/div[2]/button[2]'))
      .click();
    await driver.findElement(By.xpath('//*[@id="choix"]')).click();
    await driver.findElement(By.xpath('//*[@id="choix"]/option[3]')).click();
    await driver
      .findElement(By.xpath('//*[@id="accordion-collapse-heading-1"]/button'))
      .click();

    await driver.findElement(By.xpath('//*[@id="lastname"]')).sendKeys("Groff");
    await driver.findElement(By.xpath('//*[@id="name"]')).sendKeys("Geoffrey");
    await driver
      .findElement(By.xpath('//*[@id="username"]'))
      .sendKeys("ggroff");
    await driver
      .findElement(By.xpath('//*[@id="password"]'))
      .sendKeys("best123");
    await driver.findElement(By.xpath('//*[@id="withoutCSV"]')).click();
  });

  it("delete teacher step", async function () {
    await driver
      .findElement(By.xpath('//*[@id="accordion-collapse-heading-2"]/button'))
      .click();
    await driver.sleep(1000);
    await driver
      .findElement(
        By.xpath(
          '//*[@id="accordion-collapse-body-2"]/div/div[3]/table/tbody/tr[3]/td[5]/a'
        )
      )
      .click();
    await driver.sleep(1000);
    await driver
      .findElement(
        By.xpath(
          '//*[@id="mat-mdc-dialog-0"]/div/div/app-delete-modal/div/div/button[1]'
        )
      )
      .click();
    await driver.sleep(1000);
  });
});
