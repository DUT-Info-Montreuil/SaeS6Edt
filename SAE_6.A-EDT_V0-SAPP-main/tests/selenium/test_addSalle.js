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

describe("Responsable Edt Test", function () {
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

  it("add salle step", async function () {
    await driver
      .findElement(By.xpath('//*[@id="cal-date-nav-buttons"]/div[2]/button[2]'))
      .click();
    await selectFirst(
      driver,
      '//*[@id="add-event-modal"]/div/div/div/form/div[1]/select'
    );
    await selectFirst(
      driver,
      '//*[@id="add-event-modal"]/div/div/div/form/div[2]/select'
    );
    await selectFirst(
      driver,
      '//*[@id="add-event-modal"]/div/div/div/form/div[3]/select'
    );
    await selectFirst(
      driver,
      '//*[@id="add-event-modal"]/div/div/div/form/div[4]/select'
    );

    let dateInput = await driver.wait(
      until.elementLocated(By.id("date")),
      10000
    );
    let timeStartInput = await driver.wait(
      until.elementLocated(By.id("start")),
      10000
    );
    let timeEndInput = await driver.wait(
      until.elementLocated(By.id("end")),
      10000
    );

    let currentDate = new Date();
    let day = currentDate.getDay(); // Get the current day of the week (0 = Sunday, 1 = Monday, etc.)
    let diff = currentDate.getDate() - day + (day === 0 ? -6 : 1); // Adjust when the day is Sunday
    let monday = new Date(currentDate.setDate(diff));
    const options = { day: "2-digit", month: "2-digit", year: "numeric" };
    let formattedDate = monday.toLocaleDateString("fr-FR", options);

    // console.log(`Formatted date: ${formattedDate}`);

    let formattedStartTime = `12:00`;
    let formattedEndTime = `14:00`;

    await dateInput.sendKeys(formattedDate);
    await timeStartInput.sendKeys(formattedStartTime);
    await timeEndInput.sendKeys(formattedEndTime);
    const button_submit = await driver.findElement(
      By.xpath('//*[@id="add-event-modal"]/div/div/div/form/button')
    );
    await driver.wait(until.elementIsEnabled(button_submit));
    await button_submit.click();

    await driver.sleep(1000);

    const alert = await driver.wait(
      until.elementLocated(By.css('div[role="alert"]')),
      10000
    );
    alert.click();
    try {
      await driver.findElement(By.id("add-event-modal"));
      await driver
        .findElement(By.xpath('//*[@id="add-event-modal"]/div/div/button'))
        .click();
      assert.fail(`Failed to add course`);
    } catch (e) {
      assert.ok(true, "Course added successfully");
    }
  });

  it("modify course step", async function () {
    const calendar_xpath =
      '//*[@id="calendar-container"]/mwl-calendar-week-view/div/div/div[2]/div[1]/div[1]/div/mwl-calendar-week-view-event/div/mwl-calendar-event-title';
    let calendar = await driver.wait(
      until.elementLocated(By.xpath(calendar_xpath)),
      10000
    );

    let courses = await calendar.findElements(By.tagName("div"));
    courses[0].click();

    let timeStartInput = await driver.wait(
      until.elementLocated(By.id("start")),
      10000
    );
    let timeEndInput = await driver.wait(
      until.elementLocated(By.id("end")),
      10000
    );

    let formattedStartTime = `14:00`;
    let formattedEndTime = `16:00`;

    await timeStartInput.sendKeys(formattedStartTime);
    await timeEndInput.sendKeys(formattedEndTime);
    await driver.sleep(10000);
    // const button_submit_modify = await driver.findElement(By.xpath('//*[@id="add-event-modal"]/div/div/div/form/button'));
    await driver
      .wait(By.xpath('//*[@id="add-event-modal"]/div/div/div/form/button'))
      .click();
    // await button_submit_modify.click();
  });
});
