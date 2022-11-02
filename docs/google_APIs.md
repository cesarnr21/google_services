# Notes on Google APIs

## Gmail
response to:
```py
self.service.users().messages().list(userId = 'me', q = 'query').execute()
```
is a list of emails that match the search query

### Gmail Search Query
For a full list of Gmail search Operators, go here: <https://support.google.com/mail/answer/7190>

--------------------------------------------------------

| **Operator** | **Use** | **Example** |
|---|---|---|
| `from:` | Specify the sender | `from:email@address.com` |
| `to:` | Specify the recipient | `to:email@address.com` |
| `cc:` | Recipient of carbon copy | `cc:email@address.com` |
| `bcc:` | Recipient of blind carbon copy | `bcc:email@address.com` |
| `subject:` | Words in subject line | `subject:subject line` |
| `has:` | Emails that have attachements, Google Drive,<br>Docs, Sheets, Slides, YouTube Video, or Link | `has:attachment`<br>`has:drive`<br>`has:presentation`<br>`has:spreadsheet`<br>`has:document`<br>`has:youtube` |
| `filename:` | Attachments with a certain name or file type | `filename:pdf`<br>`filename:file1.txt` |
| `" "` | Use double qoutes for an exact search | `"text"` |
| `label:` | Messages that have a certain label | `label:important`<br>`label:inbox` |
| `in:` | To search in a specific folder | `in:inbox`<br>`in:trash`<br>`in:spam` |
| `is:` | Messages that are marked as: important, read,<br>unread, starred, snoozed. | `is:important`<br>`is:read`<br>`is:unread`<br>`is:starred`<br>`is:snoozed` |
| `after:` | Messages received/sent after a certain date | `after:2004/04/16`<br>or<br>`after:04/16/2004` |
| `before:` | Messages received/sent before a certain date | `before:2004/04/16`<br>or<br>`before:04/16/2004` |
| `older_than:`<br>and <br>`newer_than:` | Search for messages older or newer than a <br>time period using d(days), m(months), y(years) | `older_than:2d`<br>`newer_than:1d` |


