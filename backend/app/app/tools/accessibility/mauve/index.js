const fs = require("fs");
const path = require("path");
const puppeteer = require("puppeteer");
const waitForDownload = require('puppeteer-utilz').waitForDownload;
const url = process.argv[2];  // site's url to run the accessibility test 
const dest = process.argv[3]; // destination folder for the reports

const tmpPath = path.resolve(__dirname + '/tmp');
const downloadPath = path.resolve(dest);
// check and create output folder
if (!fs.existsSync(downloadPath)) {
  fs.mkdirSync(downloadPath);
}

(async () => {
  const browser = await puppeteer.launch({
    headless: "new",  // "new" or "false"
    defaultViewport: false,
    userDataDir: (__dirname + "/user_data"),
    args:[
      '--start-maximized', // you can also use '--start-fullscreen'
      '--no-sandbox'
   ],
  });

  const page = await browser.newPage();
  await page.goto('https://mauve.isti.cnr.it/singleValidation.jsp');
  await page.type('#uri', url);
  await page.click('#validate');
  const client = page._client();
  await client.send('Page.setDownloadBehavior', {
    behavior: 'allow',
    downloadPath: tmpPath 
  });

  await page.waitForSelector('a[title="download earl report"]');

  await page.click('a[title="download pdf report"]');
  await waitForDownload(tmpPath);
  fs.readdir(tmpPath, function (err, files) {
    if (err) {
        return console.log('Unable to scan directory: ' + err);
    }
    files.forEach(function (file) {
      fs.rename(tmpPath + '/' + file, downloadPath + '/' + file, (err) => {
        if (err) throw err;
      });
    });
  });

  await page.click('a[title="download earl report"]');
  await waitForDownload(tmpPath);
  fs.readdir(tmpPath, function (err, files) {
    if (err) {
        return console.log('Unable to scan directory: ' + err);
    }
    files.forEach(function (file) {
      fs.rename(tmpPath + '/' + file, downloadPath + '/' + file, (err) => {
        if (err) throw err;
      });
    });
  });

  await browser.close();

  fs.rmdir(tmpPath, (err) => {
    if (err) throw err;
  })

  /*fs.readdir(downloadPath, function (err, files) {
    if (err) {
        return console.log('Unable to scan directory: ' + err);
    } 
    files.forEach(function (file) {
        console.log(file); 
    });
  });*/
})();
