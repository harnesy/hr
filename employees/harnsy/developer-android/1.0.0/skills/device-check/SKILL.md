---
name: device-check
description: Check a mobile app change across the devices and settings real users have; small and large screens, tablets and foldables, both orientations and split screen, dark mode and high contrast, large text, the screen reader, offline and slow networks, the app being killed in the background, and permissions denied; on simulators and emulators and on real devices the person provides, with a report of what ran where, what failed with steps to reproduce, and what was not checked. Use before a release and after any change to layout, navigation, text or permissions.
---

# Device check

A screen that works on the developer's phone can break on a small one, in landscape, with large text or under a screen reader. This skill runs one change through a planned set of devices and settings, writes down exactly what was tried where, and files each problem with the steps that show it. It also says plainly which combinations were not covered, so nobody assumes they were.

**Route:** a change or a release candidate → **device-check** → a matrix of results and defect notes → the developer fixes → the failing rows are run again → the release goes on (store-release-prep).
Before this skill: a build that installs, and the list of screens the change touches. After it: a results matrix, defect notes, and a «not checked» list.

## When to use

- Before every release, on the screens the release changes.
- After a change to layout, navigation, text, images, gestures, permissions or offline handling.
- When users report a problem on one device type or with one setting.

## Inputs

- A build of the change: a debug build for quick checks, the release build before a release.
- The screens and flows the change touches.
- The device list: which device classes and OS versions matter, taken from the product's own usage data where it exists, otherwise agreed with the owner. Real devices are those the person provides; the agent does not buy, rent or log in to device farms.
- Test accounts and data, never real user accounts.

## Rules

- The device and OS list comes from who uses the product, not from a fixed list in this skill.
- Small rendering differences between devices are fine if every task still works and nothing is cut off, hidden or unreadable.
- Sizes (touch targets, text, spacing) are judged against each platform's live design guidance, read on the day and cited with its date. This skill carries no size numbers.
- Every result names the device or emulator, OS version, settings and build. «Works on Android» is not a result.
- What was not checked is written down as such, with the reason.
- Defects are recorded with steps to reproduce, expected and actual result, and a screenshot or recording where it helps.
- Test on the person's devices only with test accounts; do not change device settings the person did not agree to, and put them back afterwards.

## Steps

1. **Plan the matrix:** rows are the screens or flows; columns are the device and setting combinations. Mark which run on simulators or emulators and which need a real device (camera, sensors, performance, the real screen reader feel, push notifications).
2. **Screen sizes and shapes:** smallest supported phone, a large phone, a tablet, and a foldable or resizable window where the app supports one. Look for cut-off text, overlapping controls, content under notches, rounded corners or system bars, and layouts that waste or overflow the space.
3. **Orientation and multi-window:** rotate on every screen in the matrix; use split screen or a resized window. Check that state survives: typed text, scroll position, open dialogs.
4. **Appearance settings:** dark mode, high contrast or increased contrast, and the largest text size the OS offers. Text must grow and still fit or wrap; colours must keep meaning and contrast in both modes.
5. **Screen reader and other assistive settings:** turn on each platform's screen reader and complete the main flows by swipe and double tap only. Every control needs a spoken name, role and state; the reading order must match the visual order; focus must land somewhere sensible after a screen change. Where the platform offers switch control or voice control, try the main flow once. Run the platform's accessibility scanner on the changed screens.
6. **Gestures and navigation:** system back gesture or button on each screen, edge swipes not swallowed by the app, deep links into the changed screens.
7. **Network:** offline from start, connection lost in the middle of an action, a slow or high-latency connection. The app should say what is happening, not hang, not lose user input, and recover when the network returns.
8. **Lifecycle:** send the app to the background and return; let the OS kill it in the background (or use the developer setting that forces it) and reopen; low-memory conditions where the tools allow it. Check that the user returns to a sensible place with their data.
9. **Permissions:** deny each permission the change uses, allow it only once or while in use where the OS has those options, and revoke it in settings while the app runs. The app should explain and keep working where it can.
10. **Write the report:** the filled matrix, defect notes, and the «not checked» list.

## Checks before hand-over

- Every cell in the matrix is pass, fail or «not checked» with a reason.
- Each result names device or emulator, OS version, settings and build.
- Each defect has steps, expected, actual and evidence.
- The screen reader pass covered the main flows end to end.
- No size or threshold is stated without the live guideline and its date.
- Device settings changed for the test were put back.

## Artefacts

- `device-check/<build>-<date>.md`: the matrix, the device list and where it came from, the «not checked» list.
- `device-check/<build>-<date>/defects/`: one note per defect with screenshots or recordings.

## Hand-over

- **To the developer of the change:** the defects, ordered by how many users and how badly they are affected.
- **To the QA tester:** the matrix, for the release test plan and for exploratory testing beyond it.
- **To the designer:** layout and contrast problems that come from the design, not the code.
- **To the person who owns the devices:** which devices were used and that settings were put back.

## Per stack

- **iOS:** simulators for size, orientation, dark mode and Dynamic Type; VoiceOver on a device; the Accessibility Inspector for labels and contrast. Read Apple's Human Interface Guidelines live when a size matters.
- **Android:** emulators for phones, tablets, foldables and resizable windows, with configuration changes such as rotation and window resizing; TalkBack, Switch Access, font size and display size settings; Accessibility Scanner for touch targets, labels and contrast. Read the Material Design and Android quality guidance live when a size matters.
- **Flutter:** the semantics debugger shows what the screen reader will receive; widget tests can run the accessibility guideline checks (tap target, labels, text contrast) on each changed screen. Run TalkBack and VoiceOver on devices as well.
- **React Native:** check each control's accessibility label, hint, role and state properties, and run both TalkBack and VoiceOver; components that group children may need to be marked as one accessible element.

## Sources

Built on Android Developers documentation, «Test different screen and window sizes» and «Test your app's accessibility» (https://developer.android.com/training/testing/different-screens, https://developer.android.com/guide/topics/ui/accessibility/testing; Google LLC and the Android Open Source Project, Apache License 2.0), adapted. Portions of this page are modifications based on work created and shared by the Android Open Source Project and used according to terms described in the Creative Commons 2.5 Attribution License. Built on Flutter documentation, «Accessibility testing» (github.com/flutter/website, commit 898d84d; © The Flutter Authors, CC BY 3.0, https://creativecommons.org/licenses/by/3.0/), adapted. Built on React Native documentation, «Accessibility» (github.com/facebook/react-native-website, commit b477b73; © Meta Platforms, Inc. and affiliates, CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted. Built on GOV.UK Service Manual, «Designing for different browsers and devices», «Testing with assistive technologies» and «Making your service accessible: an introduction» (Crown copyright), adapted. Contains public sector information licensed under the Open Government Licence v3.0. This page includes information from the O*NET 31.0 Database by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA). Used under the CC BY 4.0 license. O*NET® is a trademark of USDOL/ETA. harnsy has modified all or some of this information. USDOL/ETA has not approved, endorsed, or tested these modifications.

Ideas only (no text taken): platform-design-skills (github.com/ehmo/platform-design-skills, commit dc2be82; ehmo, MIT), via Impeccable reference notes for iOS and Android (github.com/pbakaus/impeccable, commit d631a88; Paul Bakaus, Apache License 2.0).

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
