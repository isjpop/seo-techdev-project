# Wireframes

Simple ASCII wireframes for each major page.

## Login Page

```
+----------------------------------------------------------+
|                                                          |
|   Internship Tracker          +------------------------+ |
|                               |   Welcome Back         | |
|   Organize your internship    |                        | |
|   search in one place.        |   [ GitHub Login   ]   | |
|                               |   [ LinkedIn Login ]   | |
|   * Track every application   |                        | |
|   * Manage interviews         +------------------------+ |
|   * Store resume versions                                |
|   * Connect GitHub & LinkedIn                          |
|                                                          |
+----------------------------------------------------------+
```

## Dashboard

```
+--------+------------------------------------------------+
| SIDEBAR|  Dashboard                          [Avatar]  |
|        +------------------------------------------------+
| Dash   | [Total Apps] [Interviews] [Offers] [Rejections]|
| Apps   | [Response Rate %]                              |
| Docs   +------------------------------------------------+
| Profile| [Status Pie Chart]    [Apps by Month Bar Chart]|
|        +------------------------------------------------+
| Logout | Recent Apps  | Deadlines  | Interviews | Recruiter|
|        | - Google SWE | - Meta 3/1 | - Apple 2/5| - Jane @..|
|        | - Meta PM    | - Stripe 3/15             |         |
+--------+------------------------------------------------+
```

## Applications List

```
+--------+------------------------------------------------+
| SIDEBAR|  Applications                    [+ New App]   |
|        +------------------------------------------------+
|        | [Search...] [Status Filter v] [Filter] [Clear] |
|        +------------------------------------------------+
|        | Company | Position | Location | Status | Date  |
|        |---------|----------|----------|--------|-------|
|        | Google  | SWE Int  | MT View  | Applied| Jan 5 |
|        | Meta    | PM Int   | Remote   | Interview|Feb 1|
|        | Apple   | iOS Int  | Cupertino| Offer  | Dec 12|
|        +------------------------------------------------+
|        |            << Prev  Page 1/3  Next >>          |
+--------+------------------------------------------------+
```

## Application Details

```
+--------+------------------------------------------------+
| SIDEBAR|  Google — Software Engineer Intern  [Edit][Del]|
|        +------------------------------------------------+
|        | Application Details    | Recruiter              |
|        | Status: Interview      | Name: Jane Smith       |
|        | Applied: Jan 5, 2026   | Email: jane@google.com |
|        | Deadline: Mar 1, 2026  |                        |
|        | Salary: $45/hr         |                        |
|        +------------------------------------------------+
|        | Interview Timeline              [+ Add Interview]|
|        |  * Phone Screen — Feb 10, 2026 2:00 PM          |
|        |  * Technical — Feb 18, 2026 10:00 AM            |
|        +------------------------------------------------+
|        | Documents                                        |
|        |  resume_v2.pdf [Download]                        |
+--------+------------------------------------------------+
```

## Documents

```
+--------+------------------------------------------------+
| SIDEBAR|  Documents                      [+ Upload]     |
|        +------------------------------------------------+
|        | Resumes (3)              | Cover Letters (2)   |
|        | ----------------         | ----------------    |
|        | resume_v3.pdf  [DL][X]   | google_cl.pdf [DL]  |
|        | resume_v2.pdf  [DL][X]   | meta_cl.pdf   [DL]  |
|        | resume_v1.pdf  [DL][X]   |                     |
+--------+------------------------------------------------+
```

## Profile

```
+--------+------------------------------------------------+
| SIDEBAR|  Profile                                         |
|        +------------------------------------------------+
|        | [Avatar]  Jane Doe                               |
|        |           jane@example.com                       |
|        |           Member since January 2026              |
|        +------------------------------------------------+
|        | Connected Accounts                               |
|        | GitHub:    Connected as @janedoe                 |
|        | LinkedIn:  Connected                             |
|        +------------------------------------------------+
|        | GitHub Profile                                   |
|        | Name: Jane Doe | Username: @janedoe              |
|        | Repos: 24      | Bio: CS student at...           |
|        | Recent Repositories:                             |
|        |  - internship-tracker  - ml-project  - web-app   |
|        +------------------------------------------------+
|        | LinkedIn Profile                                 |
|        | Full Name: Jane Doe | Headline: CS @ University  |
+--------+------------------------------------------------+
```
