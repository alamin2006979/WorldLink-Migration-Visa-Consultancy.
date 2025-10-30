# TODO: Remove Redundant "Home" Links from Navigation Dropdowns

## Files to Edit
- [x] main.html
- [x] australia.html
- [x] usa.html
- [x] canada.html
- [x] uk.html
- [x] malaysia.html
- [x] china.html
- [x] visa-applications.html
- [x] immigration-advice.html
- [x] document-preparation.html
- [x] consultation-support.html
- [x] our-story.html
- [x] team.html
- [x] mission.html
- [x] get-in-touch.html
- [x] contact-us.html
- [x] locations.html
- [x] support.html
- [x] apply-now.html
- [x] welcome.html
- [x] hero-section.html

## Changes per File
Remove `<li><a href="main.html">Home</a></li>` from:
- Services dropdown
- About dropdown
- Contact dropdown

## Followup
- Test by opening a page in browser to verify dropdowns no longer include "Home" links.

---

# TODO: Ensure Full Responsiveness for Mobile and Desktop

## Files to Edit
- [x] main.html (already has hamburger, but verify and enhance)
- [x] australia.html
- [x] usa.html
- [x] canada.html
- [x] uk.html
- [x] malaysia.html
- [x] china.html
- [x] visa-applications.html
- [x] immigration-advice.html
- [x] document-preparation.html
- [x] consultation-support.html
- [x] our-story.html
- [x] team.html
- [x] mission.html
- [x] get-in-touch.html
- [x] contact-us.html
- [x] locations.html
- [x] support.html
- [x] apply-now.html
- [x] welcome.html
- [x] hero-section.html
- [x] universiti-putra-malaysia.html
- [x] universiti-utara-malaysia.html

## Changes per File
- Add hamburger menu for mobile navigation
- Ensure responsive layouts (flex to column on mobile, adjust padding, font sizes)
- Hide dropdowns on mobile or make them collapsible
- Adjust media queries for consistent behavior

## Followup
- Test each page on mobile and desktop views in browser

---

# TODO: Implement User Authentication System

## Files Created/Edited
- [x] auth.js (existing authentication logic)
- [x] register.html (user registration form)
- [x] login.html (user login form)
- [x] user-dashboard.html (user dashboard after login)
- [x] admin-panel.html (admin panel for managing users)
- [x] main.html (added register link to nav if not logged in)

## Features Implemented
- User registration with username, email, password
- User login with validation
- Admin login (username: admin, password: admin123)
- User dashboard with application management cards
- Admin panel with user management table
- Session persistence using localStorage
- Protected pages for users and admins
- Register link in navigation for non-logged-in users

## Followup
- Test registration, login, and dashboard access
- Verify admin panel functionality
- Check navigation updates based on login status
