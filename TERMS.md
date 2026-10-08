# harnsy catalogue contributor terms

Version `2026-10-08.1` · effective 8 October 2026

## In short

- You send an employee you built as a **pull request** to a public repository. Anyone can read it, including its history, and forks and copies cannot be called back.
- You keep it. Everyone may use its text under **CC BY 4.0 (or CC0)** and its scripts under **MIT, Apache-2.0 or CC0**.
- It is free, both ways.
- You promise it is yours to license and its sources are credited truthfully.
- An **AI agent** reviews every pull request and a **person** merges, decides blocks and answers appeals.
- Our signature means «checked against our rules», not «safe» or «approved».
- We keep no e-mail of yours. Your GitHub name, your shown name and your description are public.

## 1. Who we are and what this is

1.1 «We» is Pavel Buchnev, individual entrepreneur registered in Georgia, identification number 345621981. The catalogue is the public repository https://github.com/harnesy/hr and its copy on hr.harnsy.dev, a list of AI employees (roles with character, rules, skills and examples) that people can hire into harnsy.

1.2 An «employee» is what you send in one pull request: its text, its skills (documents and source-code scripts), its avatar image, and its credits. «You» is the person or company that sends it. If you send for a company, you confirm you may bind it. You must be at least 18. You need a GitHub account; a harnsy licence is not needed.

1.3 GitHub is a separate service with its own terms and privacy statement. They apply to what you put on GitHub. We are not GitHub and these terms do not replace theirs.

## 2. Sending an employee

2.1 Your publisher id and details are in `publishers/<id>.json`: a shown name, a short description, and the GitHub account(s) allowed to send under this id. Only those accounts may send under it. Shown name and description are public.

2.2 You send an employee by opening a pull request that follows `CONTRIBUTING.md`. Opening it, with the confirmation boxes of the template ticked, means you accept these terms in the version named in the template. If you change a box later, nothing already granted is undone (3.4).

2.3 A published version never changes: a change is a new version folder.

## 3. The licences you give

3.1 **To everyone.** You license the text of each employee (including the documents of its skills) and its avatar to everyone, worldwide, under the Creative Commons Attribution 4.0 International licence (CC BY 4.0, https://creativecommons.org/licenses/by/4.0/) or under CC0 1.0, as you state in `bundle.json` (`CC-BY-4.0` or `CC0-1.0`, and no other licence for text). You ask for credit in this form: «`<your shown name>`, hr.harnsy.dev/`<id>`@`<version>`, CC BY 4.0». The names and logos «harnsy» and «hr.harnsy.dev» and our signature are not part of this licence.

3.1a **Code.** Source-code files in a skill are licensed to everyone, worldwide, under the licence in that skill's `LICENSE` file: **MIT, Apache-2.0 or CC0-1.0, and no other**. Each code file carries your copyright line and licence identifier.

3.2 **To us.** You also give us a non-exclusive, worldwide, free licence to host, copy, check, sign, list and display the employee on hr.harnsy.dev, make it available for download and hire in harnsy, show your shown name, description, GitHub link and avatar, keep it in archives and backups, and take it off the list. It does not transfer ownership. We do not change your text; if a change is needed we ask you in the pull request.

3.3 **You keep your rights.** You may publish the same employee elsewhere and under other terms for your own copies.

3.4 **Nothing can be called back from history.** The repository is public and keeps its history. Forks, clones, GitHub's copies, web archives and copies others took under your licence stay where they are. Withdrawing an employee (section 8) stops us offering it; it does not remove it from history or from copies already taken, and the licence cannot be taken back for them.

3.5 If no copyright exists in some text (for example because a tool wrote it), you grant what rights you have, to that extent.

3.6 GitHub's terms also give GitHub and other GitHub users rights to what you post publicly (for example to view and fork it). Those rights come from GitHub's terms and are not limited by ours.

## 4. What you promise

You promise that, for each employee:

(a) **It is yours to license.** You wrote it or have the right to license it as in section 3, including your employer's or client's permission, and the terms of any tool (including AI tools) you used allow it.

(b) **Sources are lawful and credited.** Everything you adapted is licensed for this use. You followed the source rules in `CONTRIBUTING.md` (in short: ideas from ShareAlike, non-commercial, no-derivatives or unlicensed sources only, in your own words and structure; adapted material credited in `attribution` with the right licence). Your credits are complete and true. You did not copy leaked or proprietary prompts. Code you did not write is under MIT, Apache-2.0 or CC0 (or another licence that lets you relicense it as 3.1a requires) and its notice is kept.

(c) **The avatar is lawful.** It is yours or licensed to you for this, shows no real person, and uses no brand or other person's picture.

(d) **No real people or secrets.** The employee does not name, imitate or depict a real person or company without their consent, and no file contains personal data, confidential information, passwords, keys or tokens. If you committed a secret by mistake, change it at once: it stays in the history.

(e) **It is honest and safe.** The employee says it is an AI agent. It does not deceive, spam, collect data behind a login, bypass checks, take money, or act without a person's approval. It contains no hidden instructions for the agents of whoever hires it. Legal, financial, medical and HR roles prepare work and a qualified person decides. It promises no results.

(e1) **Code in skills.** Scripts are plain **source code only**: no compiled files, binaries, packed archives or minified-only or obfuscated code; no network call except those the skill names and needs for its job; nothing that runs by itself when the employee is hired (no install or post-install hooks); no reading of credentials, keys or browser data; each script does what its description says and nothing else.

(f) **Your name is true to you.** Your shown name, description and GitHub link do not impersonate another person or company and do not use another's trademark. The GitHub account is yours.

(g) **What you tell us is accurate:** the licence field, the credits, the description.

## 5. How we review

5.1 Every pull request goes through an automatic check that only reads the files and never runs anything from the pull request. Then an **AI agent** reviews it against the published rules and posts the review from the GitHub account of Pavel Buchnev; the first line of every review says it was written by an AI. The verdict is: approve for merge, changes requested, or rejected. The AI agent never merges.

5.2 **A person reads the review and merges or closes the pull request.** Merging is the decision to accept.

5.3 «Changes requested» means fix it in the same pull request, as often as you like. A rejection is final for that employee when it is a near-copy or has a harmful purpose.

5.4 After a merge, our server checks the employee again, signs it and publishes it on hr.harnsy.dev, normally within an hour. We do not promise a review time and we are not obliged to accept or publish anything.

5.5 **Our signature** means hr.harnsy.dev reviewed the employee against these rules at that time. It is not a guarantee, certification or endorsement of accuracy, safety or fitness, and you must not say it is. Everyone can read the employee's files, including its scripts, in the repository.

5.6 **Reasons.** Whenever we reject, close, revoke, restrict or block, we say in a comment on the pull request: what we did, the facts, the rule in these terms it rests on, whether an automated tool (the AI reviewer) took part, and how to appeal.

## 6. Taking down and blocking

6.1 We may withdraw a published version (an entry in `revoked.json`), close your pull requests, or block you from sending, when: you break section 4; someone makes a well-founded claim about it; the law requires it; a harm is found after publication; or you send a stream of junk.

6.2 We block at once for a harmful employee (for example one that pulls keys or data, deceives its users, or hides instructions for the hirer's agents) and for impersonating a real person or company. For a false licence or credits, or for copying, we block after the second case. A block covers you and accounts you control.

6.3 The AI reviewer recommends; **a person confirms every block**.

6.4 A withdrawn version is marked as withdrawn on hr.harnsy.dev with a short public reason category (for example «content rules», «rights claim», «withdrawn by publisher») and no further details about you. A block is shown in your publisher file as a mark with a date, without reasons. People who already hired a withdrawn employee keep their copy; harnsy shows the mark.

## 7. Appeals and reports

7.1 **Appeal.** Comment on the pull request, open an Issue in the repository, or write to hello@harnsy.dev. A person, not the AI reviewer, looks at it again and answers with reasons. You can also use any rights you have under law. Issues are public: do not put personal data in them; use e-mail for that.

7.2 **Report.** Anyone can report an employee. Please write to hello@harnsy.dev (a report contains the reporter's name and e-mail, so an Issue is not the right place) with: why it is unlawful or breaks these terms; its exact address; the reporter's name and e-mail; and a statement that they believe in good faith that the report is accurate and complete. We may hide the employee while we look, tell the publisher in the pull request, and tell the reporter what is already public: your shown name and GitHub account. A rights holder may also notify GitHub under GitHub's own rules.

## 8. When you stop

8.1 You may withdraw any version at any time by a pull request that adds it to `revoked.json` (section 3.4 applies).

8.2 To leave completely, withdraw your employees and ask at hello@harnsy.dev to remove your publisher file. We remove it from the current files and from hr.harnsy.dev; history and copies stay (section 10.6).

8.3 We may stop running the catalogue or delist employees. Copies already taken stay licensed. Where we can, we say so in the repository first.

## 9. Money, no partnership

9.1 Publishing is free. We pay you nothing and you pay us nothing. If we ever offer paid employees, it will be under new terms you accept first.

9.2 You are not our employee, partner or agent. We choose how to list, order and remove employees.

## 10. Your data

10.1 **Who is responsible.** Pavel Buchnev, individual entrepreneur, Georgia, for our part. Contact: hello@harnsy.dev. GitHub is responsible for its own service and your account there.

10.2 **What is public, and where.**
- On GitHub: your GitHub account name, your pull requests and comments, the files you send, your shown name, description and avatar, and the author name and e-mail written in your commits. GitHub offers a private «noreply» e-mail address for commits; we advise you to use it.
- On hr.harnsy.dev: your shown name, description, avatar, a link to your GitHub account, and your employees.
- Inside the files and in copies others take: the «© shown name» line and the credit.

10.3 **What we keep ourselves.** A copy of the repository on our server (Hetzner, Germany); review notes (public comments); the record of each merge (pull request, commit, account, time, hash of these terms), kept as long as the employee is listed; a block record, if any; letters you send us. We collect **no e-mail** from you. Technical records: the web server of hr.harnsy.dev logs each request (IP address, time, address requested, browser) and keeps the log for 14 days; the server's journal of catalogue updates names commits, employee ids and times, nothing about you beyond what is public. The automatic check of a pull request runs on GitHub and keeps nothing on our server.

10.4 **Why.** To run the catalogue and your contribution (contract), to prevent abuse, keep block records and defend claims (our legitimate interest), and where the law requires.

10.5 **Who else.** The AI review is done by an agent run by us on Anthropic's Claude (through Claude Code). It reads the pull request and your publisher file, which are already public; it does not receive e-mail from you. Reporters as in 7.2 and authorities where the law requires. We do not sell data.

10.6 **How long and your rights.** Letters you send us: 6 months after the last one. Our working copies of closed or rejected pull requests: 30 days after the decision. A block record: 1 year after the decision; then the block mark is removed from the current files and you may send again. The pull request itself, its comments, the repository history and forks stay on GitHub and with others and we cannot erase them. You can ask at hello@harnsy.dev to see, correct, delete or restrict what we hold, or object. We remove what we can from the current files and from hr.harnsy.dev. In a serious case (a secret, someone else's personal data, a court order) we may also rewrite the repository history or ask GitHub to remove content. You may complain to the data protection authority of Georgia or, if you live in the EU or UK, to your own.

10.7 **Decisions.** The AI reviewer can request changes or reject. It cannot block you or merge. A person decides blocks, merges and appeals.

## 11. Liability

11.1 The catalogue is free and provided «as is». We do not promise it will be available, that an employee will be accepted or published, or how many people will hire it.

11.2 You are responsible for what you send. You will cover our reasonable costs from a third party's claim caused by your breach of section 4, as far as the law allows.

11.3 Nothing in these terms limits liability that cannot be limited by law. Otherwise we are not liable for lost profit or indirect loss, and our liability for any other loss is limited to 100 euros.

## 12. Changes to these terms

The terms live in the repository as `TERMS.md`; every version stays in its history and the old versions stay readable. The pull request template names the version. The version current when you open or update a pull request applies to it. A change never reduces a licence already granted for copies already taken.

## 13. Law

These terms are governed by the laws of Georgia and the courts of Tbilisi have jurisdiction. The mandatory consumer rights of the country where you live stay. If a translation differs, the English text applies. Contact: hello@harnsy.dev.
