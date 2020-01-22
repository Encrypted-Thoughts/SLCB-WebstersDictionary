# SLCB Webster's Dictionary

The Webster's Dictionary Parameter allows for creating custom commands to get the Websters definition of 
a word for use in custom commands as a parameter

## Installing

This script was built for use with Streamlabs Chatbot.
Follow instructions on how to install custom script packs at:
https://github.com/StreamlabsSupport/Streamlabs-Chatbot/wiki/Prepare-&-Import-Scripts

Click [Here](https://github.com/Encrypted-Thoughts/SLCB-WebstersDictionary/blob/master/WebstersDictionary.zip?raw=true) to download the script pack.

## Use

Once installed the below parameter can be inserted into custom commands created in SLCB.
In custom script parameters a character length on definition can be set.
This allows long definitions to be limited so the bot doesn't spam chat with multiple messages.

```
$dictionary(
    string   # Word: The word that the parameter should retrieve the definition of.
)

Example Command: !command add !dictionary $dictionary($msg)
```

Example in twitch chat:

![exspample](https://user-images.githubusercontent.com/50642352/72930585-d978a900-3d21-11ea-8409-2a6f8003e68f.png)

## Author

EncryptedThoughts - [Twitch](https://www.twitch.tv/encryptedthoughts)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

