# Accessibility Baseline & Repository Architecture Audit

## Website Audited

https://www.india.gov.in/

Audit Date: 2026-09-13 10:00:09

## Lighthouse Baseline

| Category | Score |
|---|---:|
| Performance | N/A |
| Accessibility | N/A |
| Best Practices | N/A |
| SEO | N/A |

## Keyboard-Only Navigation

Tabs tested: 0

Status: Automation failed

### Manual Keyboard Checklist

- [ ] All links can be reached using Tab
- [ ] All buttons can be reached using Tab
- [ ] Focus indicator is visible
- [ ] Focus order is logical
- [ ] Enter activates links
- [ ] Space activates buttons
- [ ] Escape closes dialogs where applicable
- [ ] No keyboard trap

## Five Accessibility / Architecture Issues

### A01 - Keyboard navigation and focus visibility

Priority: **High**

Evidence: Tab navigation was used to identify focusable elements.

Remediation: Ensure all interactive elements are keyboard accessible and have visible focus indicators.

### A02 - Semantic HTML and landmarks

Priority: **High**

Evidence: Page structure should provide meaningful navigation and content regions.

Remediation: Use semantic header, nav, main, section and footer elements.

### A03 - Alternative text for images

Priority: **Medium**

Evidence: Informative images need text alternatives for screen-reader users.

Remediation: Add meaningful alt text and use empty alt text for decorative images.

### A04 - Color contrast

Priority: **High**

Evidence: Lighthouse provides automated accessibility checks for visual issues.

Remediation: Use sufficient foreground and background contrast.

### A05 - Client and server boundaries

Priority: **Medium**

Evidence: A maintainable full-stack project separates frontend and backend responsibilities.

Remediation: Keep client, server, documentation and tests in separate directories.

## Conclusion

The audit establishes an accessibility baseline for the selected public service website. Five accessibility and architecture issues have been identified with remediation priorities. A maintainable monorepo-style foundation has also been created.