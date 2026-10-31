---
name: store-release-prep
description: Prepare a mobile app release candidate and its store paperwork as drafts for the person who publishes; check version and build numbers and the release build settings, draft release notes and a screenshot list, draft the store privacy answers from what the code, manifest, permissions and bundled libraries show with every unknown marked, and list the store policy points to re-read on release day. The person signs, uploads and submits; the agent never holds signing keys, store accounts or credentials. Use before every store release of an iOS, Android or cross-platform app.
---

# Store release preparation

A store release fails late for dull reasons: a build number that was already used, a debug flag left on, a permission nobody can explain, privacy answers that do not match what the app sends. This skill finds those before the person who owns the store account sits down to publish. Everything it produces is a draft with its evidence; the person checks it, signs the build, uploads it and submits it.

**Route:** a release scope → **store-release-prep** → release candidate built and tested, drafts ready → the person signs, uploads and submits → the store's review → the release notes go out with the listing.
Before this skill: what goes into the release, and the commit it is built from. After it: a release folder of drafts and checks for the person, and nothing sent anywhere.

## When to use

- Before every release to an app store, including small updates: privacy answers must match each new version.
- When a new library, SDK or permission is added, even between releases: the privacy draft changes with it.

## Inputs

- The release scope and the commit the candidate is built from.
- The previous release's version and build numbers, release notes and privacy answers, as the person shares them (copied out of the store console by the person, not fetched by the agent).
- The app's manifest or property list, build configuration, permission list and dependency lock files.
- The policies and listing texts the person or the ASO specialist owns.

## Rules

- **The person signs, uploads and submits.** The agent never creates, holds, reads or copies signing keys, keystores, certificates, upload keys, provisioning profiles, passwords or store credentials, and never logs in to a store console. If a step needs any of these, it goes to the person as a written step.
- Signing material and its passwords never go into the repository, into notes or into chat. If you find any in the code, stop and tell the owner.
- Privacy answers are drafted only from evidence: code, manifest, permissions, network calls, bundled libraries and their own published data notes. Each answer cites where it came from. Anything that cannot be seen in the code (server-side retention, what a back end does with the data, legal basis) is marked «unknown — person to confirm».
- Every draft is labelled «draft from code as of commit <hash>, <date>».
- Store policy points are dated facts: section number and title, page date, link. Policy text is not copied. On release day the person or the agent re-reads the live pages, because they change.
- Nothing promises approval, review time or ranking. No claim that the app «complies» with a store policy or a law; the draft lists what was checked.

## Steps

1. **Fix the candidate:** the commit, the branch, and a clean build from it.
2. **Version and build numbers:** the user-facing version follows the project's scheme; the build number is higher than any build uploaded before (ask the person for the last one). Check that every target and platform carries the same numbers where the project expects it.
3. **Release build settings:** debug flags and debug-only menus off; logging reduced to what the release should keep; test endpoints and feature flags set for production; code shrinking and obfuscation as the project configures them, with the mapping or symbol files kept for crash reports; app identifier, display name, icons and launch screen correct.
4. **Permissions review:** list every permission the app and its libraries request, the reason string shown to users, and the code that needs it. Flag permissions with no use in the code, and libraries that add permissions on their own.
5. **Build and test the release build** on a device the person provides or on an emulator or simulator: install, first launch, sign-in, the main flows, upgrade from the previous version if possible. Release builds behave differently from debug builds; this run is not optional. For the wider device matrix use device-check.
6. **Privacy draft:** for each data type the store asks about (contact details, identifiers, location, health, financial, usage, diagnostics, user content and others on the current form), walk the evidence: permissions, platform APIs called, data sent over the network, and each bundled library and SDK with its own published data notes. Record collected or not, shared or not, purpose, linked to the user or not, optional or not, with the file or library that shows it. Mark every gap «unknown».
7. **Release notes draft:** what changed for users, in plain words, from the release scope; no internal ticket ids; no promises of what is coming next. Listing text and keywords belong to the ASO specialist if the team has one.
8. **Screenshots list:** which screens changed and need new store screenshots, per device class and language the listing uses. The images and their order are the person's or the ASO specialist's call.
9. **Policy checklist:** for each store, the sections that this release touches, by number and title, with the page date and link (see Per stack). Add a line «re-read live pages on release day».
10. **Write the hand-over** for the person: the candidate, the drafts, the open unknowns, and the manual steps that are theirs (sign, upload, fill the forms, submit, release).

## Checks before hand-over

- Version and build numbers are set and the build number is new.
- The release build was installed and its main flows run; what was not run is listed.
- Every permission has a reason and a code use, or is flagged.
- Every privacy answer cites evidence or says «unknown»; the draft carries its commit and date.
- No signing material, password or credential was touched, stored or shown.
- Policy points are dated, with links, and no policy text is copied.

## Artefacts

- `release/<version>/candidate.md`: commit, build numbers, build settings checked, release-build test results.
- `release/<version>/privacy-draft.md`: per store, per data type, answer, evidence, unknowns; header «draft from code as of commit <hash>, <date>».
- `release/<version>/release-notes-draft.md` and `release/<version>/screenshots.md`.
- `release/<version>/policy-check.md`: sections, page dates, links, and the release-day re-read line.

## Hand-over

- **To the person who publishes:** the release folder and the list of steps that are theirs: sign, upload, fill in the privacy forms, submit, release.
- **To the ASO specialist,** when the team has one: release notes draft and the screenshots list, for the listing text and images.
- **To the release manager:** the candidate status and open unknowns.
- **To devops:** anything about signing infrastructure or build pipelines.
- **To the QA tester:** the release build for a test pass beyond the main flows.

## Per stack

- **iOS (App Store):** facts as of 9 October 2026 from Apple's «App privacy details on the App Store» page: privacy answers are needed for new apps and for updates, they include data collected by third-party partners and SDKs in the app, data used only for app functionality still counts, and the developer must keep the answers up to date. App Review Guidelines (page «Last Updated: June 8, 2026», https://developer.apple.com/app-store/review/guidelines/) sections to re-read for most releases: 2.1 App Completeness, 2.3 Accurate Metadata, 5.1.1 Data Collection and Storage, 5.1.2 Data Use and Sharing. Archive the build in Xcode with the release configuration; the person signs and uploads it, for example to TestFlight first.
- **Android (Google Play):** facts as of 9 October 2026 from the Play Console Help page on the Data safety section (link in Sources): every app on Play declares how it collects and shares user data, including data handled by third-party libraries and SDKs, and the developer is responsible for complete and accurate answers; SDK providers' own data notes are a starting point. The Android release checklist: turn off logging and debugging, set `versionCode` and `versionName`, review the permissions in the manifest, enable shrinking as configured, and test the release build. The person builds the signed app bundle with their own upload key and uploads it, for example to an internal test track first.
- **Flutter:** check the bundle ID and application ID, the version and build number in `pubspec.yaml`, icons and launch image, the Android manifest and Gradle release config, and the iOS project settings; then build the iOS archive or the Android app bundle. The Flutter docs say the keystore and its passwords stay private and out of source control; here they stay with the person.
- **React Native:** build with the release scheme or configuration and test the release build on a device before upload. The Android upload key and its signing configuration stay with the person; nothing of it is committed. Review the permissions the template and libraries add by default.

## Sources

Built on Android Developers documentation, «Prepare your app for release» and «Declare your app's data use» (https://developer.android.com/studio/publish/preparing, https://developer.android.com/privacy-and-security/declare-data-use; Google LLC and the Android Open Source Project, Apache License 2.0), adapted. Portions of this page are modifications based on work created and shared by the Android Open Source Project and used according to terms described in the Creative Commons 2.5 Attribution License. Built on Flutter documentation, «Build and release an iOS app» and «Build and release an Android app» (github.com/flutter/website, commit 898d84d; © The Flutter Authors, CC BY 3.0, https://creativecommons.org/licenses/by/3.0/), adapted. Built on React Native documentation, «Publishing to Apple App Store» and «Publishing to Google Play Store» (github.com/facebook/react-native-website, commit b477b73; © Meta Platforms, Inc. and affiliates, CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted.

Store policy facts only (no text taken, ideas only): Apple, «App Review Guidelines» and «App privacy details on the App Store» (developer.apple.com, © Apple Inc.); Google Play Console Help, «Provide information for Google Play's Data safety section» (https://support.google.com/googleplay/android-developer/answer/10787469, © Google).

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
