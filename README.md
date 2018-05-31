# DAC
Convert your digital music libraries to a Discogs wantlist. This is a
rudimentary command-line client -- a web interface that will be much easier to
use is coming.

## Prerequisites
- Vagrant
- VirtualBox (or other Vagrant provider)

## Installing
```
vagrant up
```

## Services supported
- Spotify

## Services in progress
- Tidal
- Google Play

## How to use
- Rename docker-compose.yml.sample to docker-compose.yml
- Discogs
    - Generate a user-token from the
      [developer settings on the Discogs website](https://www.discogs.com/settings/developers)
    - Replace the DISCOGS_USER_TOKEN placeholder in the docker-compose file
- If using Spotify:
    - Create a new application and receive your client id and secret using the
    [developer dashboard on the Spotify website](https://developer.spotify.com/dashboard/applications)
    - Replace the SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET placeholders
    in the docker-compose file
    - Add http://localhost as a Redirect URI in your application settings.
        - After logging in, you will copy the resulting Redirect URL and provide
        it to DAC
    - Replace the SPOTIPY_REDIRECT_URI placeholder with the Redirect URI you
    provided above
    - Replace the SPOTIFY_USERNAME placeholder with your Spotify username
- Run the command line client
    - SSH into the Vagrant box:

        ```
        vagrant ssh
        ```

    - Run bash in our Docker container

        ```
        docker exec -it vagrant_app_1 /bin/bash
        ```

    - Run the command-line client, specifying the service desired

        ```
        python dac.py (-s | -t)
        ```
- If any albums cannot be saved to your wantlist, they will listed after
all other albums have been added


## Built With
- [Discogs Python API](https://github.com/discogs/discogs_client) -
Official Discogs Python API
- [Spotipy](http://spotipy.readthedocs.io/en/latest/#) -
Spotify Python API
- [tidalapi](https://pythonhosted.org/tidalapi/#) -
Unofficial Tidal Python API

## License
This project is licensed under the MIT license -
see the [LICENSE.md](LICENSE.md) for details
