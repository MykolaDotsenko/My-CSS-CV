import AxeBuilder from "@axe-core/playwright";
import { expect, test } from "@playwright/test";

test.beforeEach(async ({ page }) => {
  const consoleErrors = [];
  page.on("console", (message) => {
    if (message.type() === "error") {
      consoleErrors.push(message.text());
    }
  });

  const pageErrors = [];
  page.on("pageerror", (error) => pageErrors.push(error.message));

  await page.goto("/");

  expect(pageErrors).toEqual([]);
  expect(consoleErrors).toEqual([]);
});

test("renders the recruiter-facing content without horizontal overflow", async ({ page }) => {
  await expect(page.getByRole("heading", { level: 1, name: "Mykola Dotsenko" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Production outcomes" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Software engineering trajectory" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Projects that show how I engineer" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Software engineering" })).toBeVisible();

  const overflows = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
  expect(overflows).toBe(false);
});

test("exposes the expected professional and project destinations", async ({ page }) => {
  const expected = [
    "https://github.com/MykolaDotsenko",
    "https://www.linkedin.com/in/mykola-dotsenko/",
    "https://github.com/MykolaDotsenko/DjangoMovieProject",
    "https://github.com/MykolaDotsenko/reaktor-mykola",
    "https://github.com/MykolaDotsenko/JunaLippu",
  ];

  const hrefs = await page.locator("a").evaluateAll((links) =>
    links.map((link) => link.href)
  );

  for (const url of expected) {
    expect(hrefs).toContain(url);
  }
});

test("has no serious or critical WCAG A/AA violations", async ({ page }) => {
  const results = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
    .analyze();

  const blocking = results.violations.filter(
    (violation) => violation.impact === "serious" || violation.impact === "critical"
  );

  expect(blocking).toEqual([]);
});

test("keeps print media clean and generates an A4 PDF", async ({ page, browserName }) => {
  test.skip(browserName !== "chromium", "PDF generation is Chromium-only.");

  await page.emulateMedia({ media: "print" });

  await expect(page.locator(".page-footer")).toBeHidden();
  await expect(page.locator(".contact-section")).toBeHidden();

  const boxShadow = await page.locator(".resume").evaluate(
    (element) => getComputedStyle(element).boxShadow
  );
  expect(boxShadow).toBe("none");

  const pdf = await page.pdf({
    format: "A4",
    printBackground: true,
    preferCSSPageSize: true,
  });

  expect(pdf.byteLength).toBeGreaterThan(20_000);
});
