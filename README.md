# article-picker
Download article online and transfer it to markdown, not just html to markdown, support advance features.

## Options
The options are not too much, since I'm against too complicated parameter list.
```
Usage: main.py [-o filename] [-n] url

Options:
  -h, --help            show this help message and exit
  -o FILE, --outfile=FILE
                        file to write data
  -n, --nohead          do not read header
  -m METHOD, --method=METHOD
                        1: Basic Html2Text Parser (DEFAULT) 2: Forked
                        Html2Text Parser 3: AntiMarkdown Parser
```
There is not too much to say, but I very much hope that anyone can provide a better conversion library to convert html to markdown.

## Rules
Rule Sample:
```JSON
{
  "name": "WeiXin",
  "author": "Skactor",
  "url": "mp.weixin.qq.com",
  "regex": false,
  "header": {
    "title": "<title>(.+?)</title>",
    "author": "nickname ?= ?\"(.+?)\";",
    "date": {
      "value": "ct ?= ?\"(\\d+)\"",
      "filter": [
        "ts2dt"
      ]
    }
  },
  "content": {
    "begin": "<div class=\"rich_media_content \" id=\"js_content\">",
    "end": "<script nonce="
  }
}
```
### Match Pattern
`url` parameter can be the pattern you wan't to match the rule, or just using string check to match.

You can use the `regex` parameter to specify match mode.

### Header Parse
The `header` array parameter is used to print header in result.

It now just support **single matched regular expression**, the first matcher will be considered as result.

By the way, It support advanced usage which uses `filter` and `value` to handle your header.

In the above sample, we can see this
```JSON
"date": {
  "value": "ct ?= ?\"(\\d+)\"",
  "filter": [
    "ts2dt"
  ]
}
```
this is the usage of filter in header parse, the `ts2dt` function is defined in `lib/filter.py`, you can add your own function if necessary. But remember **Just one parameter is supported now**.

### Content Parse
#### Clean Or Replace
```JSON
"replace": {
  "data-original": "src",
  "src=\"http://www.freebuf.com/buf/themes/freebuf/images/grey.gif\" ": ""
}
```
This above `replace` parameter is used when you wan't the process your content **before** convert it to markdown.

#### Content interception
```
"content": {
  "begin": "<div class=\"rich_media_content \" id=\"js_content\">",
  "end": "<script nonce="
}
```
Like the `Content` parameter shown above, you can specify the begin and end string of content. This is always useful and should be specify each time.
## Reference
Libs now:
 - https://github.com/aaronsw/html2text
 - https://github.com/Alir3z4/html2text/
 - https://github.com/Crossway/antimarkdown/
