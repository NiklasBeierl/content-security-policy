# Handling Content-Security-Policy with less footguns

Create, maintain, parse and
manipulate [Content Security Policies](https://developer.mozilla.org/docs/Web/HTTP/Headers/Content-Security-Policy).

## For site developers / operators

Content-Security-Policy (CSP) is a very effective mitigation against cross site
scripting (XSS). It should be right up there with HTTPS on your list of mitigations to
deploy on your site. Depending on your applicaiton, creating and maintaining a CSP can
be somewhat frickle and annoying. This library hopes to alleviate that pain by allowing
you to create (or automate creating) your policy as code.

### Django integration

There is a brand-new integration with django. Documentation outside the source-code is
still a TODO (PRs welcome). You can get an idea from the corresponding
[tests](content_security_policy/django/test).

```sh
pip install content-security-policy[django]
```

## For researchers

Parse, analyze and manipulate csp strings.

# Principles

## Immutability

Any policy / directive / directive value object you create is immutable.

## Strict construction

> :warning: This feature is still being developed! There are a lot of things not yet
> being validated.

When explicitly constructing objects with invalid values, errors will be raised! For
example, you can not construct a nonce source expression with non-base64 characters.

```
>>> NonceSrc("ungültig")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<redacted>/content_security_policy/values.py", line 55, in __init__
    raise BadSourceExpression(
content_security_policy.exceptions.BadSourceExpression: Nonce value 'ungültig' does not match ([A-Za-z]|[0-9]|[+\/\-_]){2, 0}={0, 2}
```

## Lenient parsing

The parsing functions should be able to take any string and "somehow" parse it. If
(parts of) the string can not be matched to a known directive or directive value,
instances of `UnrecognizedDirective` and `UnrecognizedValueItem` will represent those
parts of the string.

```python
from content_security_policy.parse import *

policy_string = "script-src 'strict-dynamic' garbage; whatsthis directive 'supposedTobe'?"

policy = policy_from_string(policy_string)

for directive in policy:
    print(f"Name: {directive.name}\nType: {directive.__class__.__name__}\nValues:")
    for val in directive:
        print(f"\tType: {val.__class__.__name__}\n\tValue: {val}\n")
```

```
Name: script-src
Type: ScriptSrc
Values:
        Type: KeywordSource
        Value: 'strict-dynamic'

        Type: UnrecognizedValueItem
        Value: garbage

Name: whatsthis
Type: UnrecognizedDirective
Values:
        Type: UnrecognizedValueItem
        Value: directive

        Type: UnrecognizedValueItem
        Value: 'supposedTobe'?
```

# Usage

There are classes for policy, different kinds of directives and directive values.

> :information_source: Proper documentation is still a TODO.

For now, you will need to check the source code / rely on auto-completion.
The [tests](./content_security_policy/test) cover a lot of the intended use-cases.
Some of the general ideas are hopefully well conveyed in these examples:

### Something very simple

```python
from content_security_policy import *

policy = Policy(
    DefaultSrc(KeywordSource.self), FrameAncestors(SelfSrc), ObjectSrc(NoneSrc)
)
assert str(policy) == "default-src 'self'; frame-ancestors 'self'; object-src 'none'"
```

### Something a little more dynamic

```python
from content_security_policy import *

script_src = ScriptSrc()

for url in ["https://example.com/some-lib.js", "https://example-cdn.com/other-lib.js"]:
    script_src += HostSrc(url)

script_src += SelfSrc

assert str(
    script_src) == "script-src https://example.com/some-lib.js https://example-cdn.com/other-lib.js 'self'"
```

### Parse and manipulate

```python
from content_security_policy import *
from content_security_policy.parse import *

policy = policy_from_string(
    "deFault-src 'self'; Frame-Ancestors\t 'self'; \t object-src 'none'"
)

frame_ancestors = policy["frame-ancestors"]
# alternatively:
# frame_ancestors = policy.frame_ancestors
frame_ancestors += HostSrc("https://example.com")

# Splice frame-ancestors from the policy
policy -= FrameAncestors

# Adding always appends the directive at the end!
policy += frame_ancestors

# Notice that whitespace and capitalization was preserved!
assert str(
    policy) == "deFault-src 'self'; \t object-src 'none'; Frame-Ancestors\t 'self' https://example.com"
```

# Installation

```shell
pip install content-security-policy
```

# Priorities

## 1. Correctness

As per the license, there is no warranty, but the number one rule is:
> If you don't deliberately bypass any safeguards when constructing a CSP
> programmatically, the string you obtain from it will be according to spec.

Note that this does not mean your CSP will be _effective_! A `script-src`
with `'unsafe-inline'` is correct according to the spec, but you loose any XSS
protection CSP could have provided you!

## 2. Useful

Handling the objects created with this library should be reasonably intuitive and "
pythonic".
