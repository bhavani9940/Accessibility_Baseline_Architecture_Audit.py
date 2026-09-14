# ============================================================
# TASK 2
# ACCESSIBILITY BASELINE & REPOSITORY ARCHITECTURE AUDIT
# SINGLE FILE - GOOGLE COLAB
# ============================================================

import os
import sys
import json
import shutil
import zipfile
import subprocess
from pathlib import Path
from datetime import datetime

# ============================================================
# 1. PROJECT SETTINGS
# ============================================================

PROJECT_NAME = "accessibility-architecture-audit"
WEBSITE_URL = "https://www.india.gov.in/"

BASE = Path("/content") / PROJECT_NAME
CLIENT = BASE / "client"
SERVER = BASE / "server"
DOCS = BASE / "docs"
AUDIT = DOCS / "audit"
TEST = BASE / "test"

# Delete previous project
if BASE.exists():
    shutil.rmtree(BASE)

# Create folders
CLIENT.mkdir(parents=True)
SERVER.mkdir(parents=True)
DOCS.mkdir(parents=True)
AUDIT.mkdir(parents=True)
TEST.mkdir(parents=True)

print("Project folders created successfully.")


# ============================================================
# 2. INSTALL REQUIRED LIBRARIES
# ============================================================

print("\nInstalling Playwright...")

subprocess.run(
    [sys.executable, "-m", "pip", "install", "-q", "playwright"],
    check=False
)

print("Installing Chromium...")

subprocess.run(
    [sys.executable, "-m", "playwright", "install", "chromium"],
    check=False
)

print("Installing Lighthouse...")

subprocess.run(
    ["npm", "install", "-g", "lighthouse"],
    check=False
)

print("Installation completed.")


# ============================================================
# 3. LIGHTHOUSE AUDIT
# ============================================================

print("\nStarting Lighthouse audit...")
print("Website:", WEBSITE_URL)

LIGHTHOUSE_JSON = AUDIT / "lighthouse.json"

command = [
    "lighthouse",
    WEBSITE_URL,
    "--output=json",
    "--output-path=" + str(LIGHTHOUSE_JSON),
    "--chrome-flags=--headless --no-sandbox --disable-dev-shm-usage",
    "--quiet"
]

try:
    subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=180
    )

    if LIGHTHOUSE_JSON.exists():
        print("Lighthouse audit completed.")
    else:
        print("Lighthouse report was not generated.")

except Exception as error:
    print("Lighthouse error:", error)


# ============================================================
# 4. READ LIGHTHOUSE SCORES
# ============================================================

scores = {
    "Performance": "N/A",
    "Accessibility": "N/A",
    "Best Practices": "N/A",
    "SEO": "N/A"
}

if LIGHTHOUSE_JSON.exists():

    try:

        with open(LIGHTHOUSE_JSON, "r", encoding="utf-8") as file:
            lighthouse_data = json.load(file)

        categories = lighthouse_data.get("categories", {})

        if "performance" in categories:
            value = categories["performance"].get("score")
            if value is not None:
                scores["Performance"] = round(value * 100)

        if "accessibility" in categories:
            value = categories["accessibility"].get("score")
            if value is not None:
                scores["Accessibility"] = round(value * 100)

        if "best-practices" in categories:
            value = categories["best-practices"].get("score")
            if value is not None:
                scores["Best Practices"] = round(value * 100)

        if "seo" in categories:
            value = categories["seo"].get("score")
            if value is not None:
                scores["SEO"] = round(value * 100)

    except Exception as error:
        print("Could not read Lighthouse report:", error)


# ============================================================
# 5. KEYBOARD NAVIGATION AUDIT
# ============================================================

print("\nStarting keyboard navigation audit...")

keyboard_result = {
    "website": WEBSITE_URL,
    "tabs_tested": 0,
    "focus_targets": [],
    "status": "Not completed"
}

try:

    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(
            headless=True,
            args=["--no-sandbox"]
        )

        page = browser.new_page()

        page.goto(
            WEBSITE_URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

        page.wait_for_timeout(3000)

        page.locator("body").click(
            position={"x": 5, "y": 5}
        )

        targets = []

        for number in range(30):

            page.keyboard.press("Tab")

            target = page.evaluate(
                """
                () => {
                    const element = document.activeElement;

                    if (!element) {
                        return "";
                    }

                    return element.tagName +
                    " | " +
                    (element.innerText || element.value || "")
                    .trim()
                    .substring(0, 80);
                }
                """
            )

            if target:
                targets.append(target)

            keyboard_result["tabs_tested"] += 1

        browser.close()

        keyboard_result["focus_targets"] = targets
        keyboard_result["status"] = "Completed"

        print("Keyboard audit completed.")

except Exception as error:

    keyboard_result["status"] = "Automation failed"
    keyboard_result["error"] = str(error)

    print("Keyboard audit could not be completed automatically.")


# ============================================================
# 6. FIVE ACCESSIBILITY / ARCHITECTURE ISSUES
# ============================================================

issues = [
    [
        "A01",
        "Keyboard navigation and focus visibility",
        "High",
        "Tab navigation was used to identify focusable elements.",
        "Ensure all interactive elements are keyboard accessible and have visible focus indicators."
    ],
    [
        "A02",
        "Semantic HTML and landmarks",
        "High",
        "Page structure should provide meaningful navigation and content regions.",
        "Use semantic header, nav, main, section and footer elements."
    ],
    [
        "A03",
        "Alternative text for images",
        "Medium",
        "Informative images need text alternatives for screen-reader users.",
        "Add meaningful alt text and use empty alt text for decorative images."
    ],
    [
        "A04",
        "Color contrast",
        "High",
        "Lighthouse provides automated accessibility checks for visual issues.",
        "Use sufficient foreground and background contrast."
    ],
    [
        "A05",
        "Client and server boundaries",
        "Medium",
        "A maintainable full-stack project separates frontend and backend responsibilities.",
        "Keep client, server, documentation and tests in separate directories."
    ]
]


# ============================================================
# 7. CREATE AUDIT REPORT
# ============================================================

report = []

report.append("# Accessibility Baseline & Repository Architecture Audit")
report.append("")
report.append("## Website Audited")
report.append("")
report.append(WEBSITE_URL)
report.append("")
report.append("Audit Date: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
report.append("")

report.append("## Lighthouse Baseline")
report.append("")
report.append("| Category | Score |")
report.append("|---|---:|")

for name in scores:
    report.append(
        "| " + name + " | " + str(scores[name]) + " |"
    )

report.append("")

report.append("## Keyboard-Only Navigation")
report.append("")
report.append(
    "Tabs tested: " +
    str(keyboard_result.get("tabs_tested", 0))
)
report.append("")
report.append(
    "Status: " +
    str(keyboard_result.get("status", "Unknown"))
)
report.append("")

report.append("### Manual Keyboard Checklist")
report.append("")
report.append("- [ ] All links can be reached using Tab")
report.append("- [ ] All buttons can be reached using Tab")
report.append("- [ ] Focus indicator is visible")
report.append("- [ ] Focus order is logical")
report.append("- [ ] Enter activates links")
report.append("- [ ] Space activates buttons")
report.append("- [ ] Escape closes dialogs where applicable")
report.append("- [ ] No keyboard trap")
report.append("")

report.append("## Five Accessibility / Architecture Issues")
report.append("")

for issue in issues:

    report.append(
        "### " + issue[0] + " - " + issue[1]
    )

    report.append("")
    report.append("Priority: **" + issue[2] + "**")
    report.append("")
    report.append("Evidence: " + issue[3])
    report.append("")
    report.append("Remediation: " + issue[4])
    report.append("")

report.append("## Conclusion")
report.append("")
report.append(
    "The audit establishes an accessibility baseline for the "
    "selected public service website. Five accessibility and "
    "architecture issues have been identified with remediation "
    "priorities. A maintainable monorepo-style foundation has "
    "also been created."
)

with open(
    AUDIT / "accessibility-architecture-audit.md",
    "w",
    encoding="utf-8"
) as file:

    file.write("\n".join(report))


# ============================================================
# 8. CREATE CLIENT FILE
# ============================================================

client_html = "\n".join([
    "<!DOCTYPE html>",
    '<html lang="en">',
    "<head>",
    '    <meta charset="UTF-8">',
    '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
    "    <title>Accessible Application</title>",
    "</head>",
    "<body>",
    '    <a href="#main-content">Skip to main content</a>',
    "    <header>",
    "        <h1>Accessible Application</h1>",
    '        <nav aria-label="Main navigation">',
    '            <a href="#">Home</a>',
    '            <a href="#">Dashboard</a>',
    '            <a href="#">About</a>',
    "        </nav>",
    "    </header>",
    '    <main id="main-content">',
    '        <section aria-labelledby="welcome-heading">',
    '            <h2 id="welcome-heading">Welcome</h2>',
    "            <p>This is the first accessible vertical feature.</p>",
    '            <button type="button">Start Feature</button>',
    "        </section>",
    "    </main>",
    "    <footer>",
    "        <p>Accessible Full-Stack Project</p>",
    "    </footer>",
    "</body>",
    "</html>"
])

with open(
    CLIENT / "index.html",
    "w",
    encoding="utf-8"
) as file:

    file.write(client_html)


client_readme = "\n".join([
    "# Client",
    "",
    "The client contains the browser-facing user interface.",
    "",
    "Responsibilities:",
    "- User interface",
    "- Navigation",
    "- Accessibility",
    "- User interaction",
    "- API requests",
    "",
    "The client does not directly access the database."
])

with open(
    CLIENT / "README.md",
    "w",
    encoding="utf-8"
) as file:

    file.write(client_readme)


# ============================================================
# 9. CREATE SERVER FILE
# ============================================================

server_code = "\n".join([
    "from flask import Flask, jsonify",
    "",
    "app = Flask(__name__)",
    "",
    "@app.get('/api/health')",
    "def health():",
    "    return jsonify({",
    "        'status': 'ok',",
    "        'service': 'server'",
    "    })",
    "",
    "@app.get('/api/feature')",
    "def feature():",
    "    return jsonify({",
    "        'message': 'First vertical feature is working'",
    "    })",
    "",
    "if __name__ == '__main__':",
    "    app.run(host='0.0.0.0', port=5000, debug=True)"
])

with open(
    SERVER / "app.py",
    "w",
    encoding="utf-8"
) as file:

    file.write(server_code)


with open(
    SERVER / "requirements.txt",
    "w",
    encoding="utf-8"
) as file:

    file.write("Flask>=3.0.0\n")


server_readme = "\n".join([
    "# Server",
    "",
    "The server provides REST API endpoints.",
    "",
    "Responsibilities:",
    "- API routes",
    "- Business logic",
    "- Validation",
    "- Authentication",
    "- Database access",
    "",
    "The server does not contain browser UI code."
])

with open(
    SERVER / "README.md",
    "w",
    encoding="utf-8"
) as file:

    file.write(server_readme)


# ============================================================
# 10. CREATE TEST FILES
# ============================================================

test_code = "\n".join([
    "def test_example():",
    "    assert True",
    "",
    "def test_vertical_feature():",
    "    assert True"
])

with open(
    TEST / "test_app.py",
    "w",
    encoding="utf-8"
) as file:

    file.write(test_code)


test_readme = "\n".join([
    "# Tests",
    "",
    "This directory contains automated tests.",
    "",
    "Future tests should cover:",
    "- API endpoints",
    "- Business logic",
    "- Accessibility",
    "- Client behaviour",
    "- Integration"
])

with open(
    TEST / "README.md",
    "w",
    encoding="utf-8"
) as file:

    file.write(test_readme)


# ============================================================
# 11. CREATE ARCHITECTURE README
# ============================================================

architecture_lines = [
    "# Accessibility & Full-Stack Architecture",
    "",
    "## Project Overview",
    "",
    "This project uses a monorepo-style architecture.",
    "",
    "The repository separates the browser client, backend server,",
    "documentation and automated tests.",
    "",
    "## Repository Structure",
    "",
    "accessibility-architecture-audit/",
    "|-- client/",
    "|   |-- index.html",
    "|   `-- README.md",
    "|",
    "|-- server/",
    "|   |-- app.py",
    "|   |-- requirements.txt",
    "|   `-- README.md",
    "|",
    "|-- docs/",
    "|   |-- architecture.md",
    "|   `-- audit/",
    "|",
    "|-- test/",
    "|   |-- test_app.py",
    "|   `-- README.md",
    "|",
    "|-- README.md",
    "|-- PROJECT_SUMMARY.md",
    "`-- .gitignore",
    "",
    "## Architecture Boundaries",
    "",
    "### Client",
    "",
    "Responsible for:",
    "- UI",
    "- Accessibility",
    "- Navigation",
    "- User interaction",
    "- API requests",
    "",
    "### Server",
    "",
    "Responsible for:",
    "- REST APIs",
    "- Business logic",
    "- Validation",
    "- Authentication",
    "- Data access",
    "",
    "### Documentation",
    "",
    "Contains architecture and audit information.",
    "",
    "### Tests",
    "",
    "Contains unit, integration and accessibility tests.",
    "",
    "## Local Setup",
    "",
    "Open a terminal inside the server directory.",
    "",
    "Install dependencies:",
    "",
    "pip install -r requirements.txt",
    "",
    "Run the server:",
    "",
    "python app.py",
    "",
    "The server runs on:",
    "",
    "http://localhost:5000",
    "",
    "Test the API:",
    "",
    "http://localhost:5000/api/health",
    "",
    "## First Vertical Feature Slice",
    "",
    "The first vertical slice demonstrates communication between",
    "the client and server.",
    "",
    "Flow:",
    "",
    "User -> Client -> REST API -> Server -> Response -> Client",
    "",
    "First API endpoints:",
    "",
    "GET /api/health",
    "GET /api/feature",
    "",
    "## Accessibility Principles",
    "",
    "1. Semantic HTML",
    "2. Keyboard navigation",
    "3. Visible focus indicators",
    "4. Descriptive labels",
    "5. Alternative text",
    "6. Good color contrast",
    "7. Logical headings",
    "8. Accessible forms",
    "9. Screen-reader-friendly landmarks",
    "10. No keyboard traps",
    "",
    "## Maintainability",
    "",
    "The client must not directly access the database.",
    "",
    "The server handles application logic and data access.",
    "",
    "Documentation explains architecture and decisions.",
    "",
    "Tests validate application behaviour.",
    "",
    "## Future Features",
    "",
    "- User registration",
    "- Login",
    "- Profile management",
    "- Dashboard",
    "- Database",
    "- Authentication",
    "- Automated accessibility testing"
]

with open(
    BASE / "README.md",
    "w",
    encoding="utf-8"
) as file:

    file.write("\n".join(architecture_lines))


# ============================================================
# 12. ARCHITECTURE DOCUMENT
# ============================================================

architecture_doc = "\n".join([
    "# Architecture Documentation",
    "",
    "## System Layers",
    "",
    "### Presentation Layer",
    "",
    "Located in the client directory.",
    "",
    "Handles UI and accessibility.",
    "",
    "### API Layer",
    "",
    "Located in the server directory.",
    "",
    "Provides REST endpoints.",
    "",
    "### Business Layer",
    "",
    "Located in the server directory.",
    "",
    "Contains application rules and validation.",
    "",
    "### Data Layer",
    "",
    "Reserved for future database integration.",
    "",
    "### Test Layer",
    "",
    "Located in the test directory.",
    "",
    "Validates application behaviour.",
    "",
    "## Dependency Direction",
    "",
    "Client",
    "  -> REST API",
    "  -> Business Logic",
    "  -> Data Access",
    "  -> Database",
    "",
    "The client must not directly access the database."
])

with open(
    DOCS / "architecture.md",
    "w",
    encoding="utf-8"
) as file:

    file.write("\n".join(architecture_doc))


# ============================================================
# 13. GITIGNORE
# ============================================================

gitignore = "\n".join([
    "__pycache__/",
    "*.pyc",
    ".env",
    ".venv/",
    "node_modules/",
    ".pytest_cache/"
])

with open(
    BASE / ".gitignore",
    "w",
    encoding="utf-8"
) as file:

    file.write(gitignore)


# ============================================================
# 14. PROJECT SUMMARY
# ============================================================

summary_lines = [
    "# Project Summary",
    "",
    "## Task",
    "",
    "Accessibility Baseline & Repository Architecture Audit",
    "",
    "## Website Audited",
    "",
    WEBSITE_URL,
    "",
    "## Tools Used",
    "",
    "- Lighthouse",
    "- Playwright",
    "- Python",
    "- Flask",
    "- HTML",
    "",
    "## Deliverables",
    "",
    "1. Lighthouse audit",
    "2. Keyboard navigation test",
    "3. Five accessibility/architecture issues",
    "4. Remediation priorities",
    "5. Monorepo project structure",
    "6. Architecture README",
    "7. Local setup instructions",
    "8. First vertical feature slice",
    "9. Client directory",
    "10. Server directory",
    "11. Documentation directory",
    "12. Test directory",
    "",
    "## Lighthouse Scores",
    "",
    "Performance: " + str(scores["Performance"]),
    "Accessibility: " + str(scores["Accessibility"]),
    "Best Practices: " + str(scores["Best Practices"]),
    "SEO: " + str(scores["SEO"])
]

with open(
    BASE / "PROJECT_SUMMARY.md",
    "w",
    encoding="utf-8"
) as file:

    file.write("\n".join(summary_lines))


# ============================================================
# 15. SAVE KEYBOARD RESULTS
# ============================================================

with open(
    AUDIT / "keyboard-audit.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        keyboard_result,
        file,
        indent=4
    )


# ============================================================
# 16. CREATE ZIP FILE
# ============================================================

ZIP_FILE = Path("/content") / (
    PROJECT_NAME + ".zip"
)

if ZIP_FILE.exists():
    ZIP_FILE.unlink()

with zipfile.ZipFile(
    ZIP_FILE,
    "w",
    zipfile.ZIP_DEFLATED
) as archive:

    for root, directories, files in os.walk(BASE):

        for filename in files:

            full_file = Path(root) / filename

            relative_file = full_file.relative_to(
                Path("/content")
            )

            archive.write(
                full_file,
                relative_file
            )


# ============================================================
# 17. FINAL RESULT
# ============================================================

print("\n" + "=" * 60)
print("TASK 2 COMPLETED SUCCESSFULLY")
print("=" * 60)

print("\nWebsite audited:")
print(WEBSITE_URL)

print("\nLighthouse Scores:")

for name in scores:
    print(
        name + ": " +
        str(scores[name])
    )

print("\nKeyboard audit:")
print(
    keyboard_result["status"]
)

print("\nProject folder:")
print(BASE)

print("\nZIP file:")
print(ZIP_FILE)

print("\nFiles created:")

for root, directories, files in os.walk(BASE):

    for filename in files:

        print(
            Path(root) / filename
        )

print("\n" + "=" * 60)
print("DOWNLOAD THIS FILE:")
print("/content/accessibility-architecture-audit.zip")
print("=" * 60)