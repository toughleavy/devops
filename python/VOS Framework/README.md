## Description

Welcome aboard fellow devops, this is where you will find the VOS Framework which you are free to use.
This repository provides scripts to help you save a massive amount of time when creating or modifiying security rules ( but not only ) on VOS.

## Motivation

Every once in a while you will have to perform anoying & time consumings tasks on your devices , i ve been there so many time  I wanted to find a way to make our life easier. Let me share a couple of examples.

- You need to create 234 security rules based on an excel sheet.
- You need to remove disabled rules on each devices in the organization (too bad there are 100 of them).
- You need to add log settings on security rules when it is missing.
- You need to enable rules with the TAG OK after they were approved (Corp approves dozen of them each week).

And the list goes on :)

## Installation and Dependencies
You will need python3 as well as differents python package. They can be installed locally with pip3
```
pip3 install json
pip3 install requests
pip3 install urllib3
pip3 install argparse
```

## Projects

| SR No | Project                                                                                                                                | Description                                             |
| ----- | -------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| 1     | [VOS Rule Edit](https://gitlab.com/versa-networks/devops/-/tree/master/python/VOS%20Framework/rule-edit)                               | Manipulate VOS rules like a pro                         |
| 2     | [VOS Rule Create](https://gitlab.com/versa-networks/devops/-/tree/master/python/VOS%20Framework/rule-create)                           | Create VOS rules at the speed of light                  |