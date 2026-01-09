# Discord Server Template & Role Manager

A Discord bot that saves and restores server structure and roles using simple commands.

## Features

- Save server category and channel layout  
- Restore channels with correct order and permissions  
- Save roles separately from templates  
- Restore roles with permissions, colors, hoist, mentionable, and positions  
- Skips undeletable channels or roles safely  
- Restricted to specific user IDs  

## Commands

Prefix: `;`

### Templates
- `;savetemplate`  
  Saves all categories, channels, positions, and permission overwrites to `template.txt`.

- `;loadtemplate`  
  Deletes existing channels and rebuilds the server from `template.txt`.

### Roles
- `;saveroles`  
  Saves all non-default, non-managed roles to `roles.txt`.

- `;loadroles`  
  Deletes existing roles and recreates them from `roles.txt`, restoring order where possible.

## Configuration

Edit these values in the script:

- `zyzo_allowed_users` – Discord user IDs allowed to run commands  
- Bot token at the bottom of the file  
- Command prefix if needed  

## Files Created

- `template.txt` – Server categories and channels  
- `roles.txt` – Server roles  

## Requirements

- Python 3.9+  
- discord.py (with message content intent enabled)  

## Notes

- Role positions are restored only if the bot’s role is high enough  
- Managed roles and @everyone are skipped  
- Errors are silently ignored to prevent crashes  
