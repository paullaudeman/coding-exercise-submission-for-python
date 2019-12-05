import argparse
from os import path
import json
import logging
import uuid
from enconders import UUIDEncoder

logging.basicConfig(level=logging.DEBUG)


class SuperMixer:
    def __init__(self, mixtape_obj, changes_obj):
        if mixtape_obj is None or not isinstance(mixtape_obj, dict):
            raise TypeError('Expected valid mixtape dictionary object.')
        if changes_obj is None or not isinstance(changes_obj, dict):
            raise TypeError('Expected valid changes dictionary object.')

        self.mixtape_obj = mixtape_obj
        self.changes_obj = changes_obj

        logging.info("SuperMixer initialized, input file loaded, changes to process loaded.")

    def find_existing_playlist(self, playlist_id):
        for playlist_to_delete in self.mixtape_obj['playlists']:
            playlist = playlist_to_delete['playlist']
            if playlist['id'] == playlist_id:
                return playlist
        logging.info(f'Playlist with id {playlist_id} was not found.')

    def delete_playlist(self, playlist_id):
        playlist = self.find_existing_playlist(playlist_id)

        if playlist is not None:
            del playlist
            logging.info(f'Playlist id {playlist_id} deleted.')

    def process_deletions(self):
        """
        Deletes existing playlists, if found
        """
        logging.info('Processing playlist deletions.')

        if 'deletions' not in self.changes_obj:
            logging.info('No deletions were found to process.')
            return

        if 'deletions' not in self.changes_obj and 'playlists' not in self.changes_obj:
            logging.info('No playlist deletions were found to process.')
            return

        for playlist_to_delete in self.changes_obj['deletions']['playlists']:
            logging.debug(f'Deleting playlist id {playlist_to_delete}.')
            self.delete_playlist(playlist_to_delete)

    def song_exists(self, song_id):
        if 'songs' not in self.mixtape_obj:
            logging.info('No songs are currently defined in the mixer.')
            return False

        for song in self.mixtape_obj['songs']:
            if song["id"] == song_id:
                return True

    def process_additions_to_existing_playlists(self):
        """
        Adds an existing song to an existing playlist
        """
        logging.info('Processing playlist additions.')

        if 'additions' not in self.changes_obj:
            logging.info('No additions were found to process.')
            return
        if len(self.changes_obj['additions']['existing_playlists_to_update']) == 0:
            logging.info('No playlists were found in the additions, nothing to do.')
            return

        # make sure we have existing playlists or skip
        if 'playlists' not in self.mixtape_obj and not len(self.mixtape_obj['playlists']) > 0:
            logging.info("No existing playlists have been defined, so we can't add new songs.")
            return

        # for each playlist defined, attempt to add the songs
        for playlist in self.changes_obj['additions']['existing_playlists_to_update']:
            # find existing playlist
            playlist_id_to_update = playlist['id']
            existing_playlist = self.find_existing_playlist(playlist_id_to_update)

            for song in playlist["songs"]:
                if self.song_exists(song):
                    existing_playlist["songs"].append(song)

    def user_exists(self, user_id):
        if 'users' not in self.mixtape_obj:
            logging.info("No users have been defined in the SuperMixer, unable to lookup user.")
            return False

        for user in self.mixtape_obj['users']:
            if user['user_id'] == user_id:
                return True

        return False

    def all_songs_exist(self, songs):
        for song in songs:
            if self.song_exists(song) is False:
                return False

        return True

    def process_new_playlists(self):
        """
        Adds a new playlist to an existing user, if the new playlist has at least one song
        """
        if 'additions' not in self.changes_obj:
            logging.info('No playlists were found to add.')
            return

        if len(self.changes_obj['additions']['new_playlists']) == 0:
            logging.info('No new playlists were found, nothing to do.')
            return

        for new_playlist in self.changes_obj['additions']['new_playlists']:
            user_id = new_playlist['user_id']

            if not self.user_exists(user_id):
                logging.warning(f'Existing user id {user_id} not found, unable to add a playlist.')
                continue

            if 'songs' not in new_playlist:
                logging.warning('Cannot add new playlist as no songs are present.')
                continue

            if len(new_playlist['songs']) == 0:
                logging.warning('New playlist must have one or more songs.')
                continue

            # any of the songs passed in might not exist. assumption here is we don't want
            # incomplete playlists, so if any of the songs they are trying to add don't exist,
            # skip and continue
            if self.all_songs_exist(new_playlist['songs']) is False:
                logging.warning(f'One or more songs do not exist, unable to create a new playlist.')
                continue

            # add new playlist
            self.mixtape_obj['playlists'].append(
                {
                    "playlist":
                    {
                        "id": uuid.uuid1(),
                        "name": new_playlist["name"],
                        "user_id": user_id,
                        "songs": new_playlist['songs']
                    }
                }
            )

    def run(self):
        self.process_deletions()
        self.process_additions_to_existing_playlists()
        self.process_new_playlists()

        # save changes
        logging.debug(f'result={self.mixtape_obj}')

        return self.mixtape_obj


if __name__ == "__main__":
    logging.info("*** Program Initializing")

    parser = argparse.ArgumentParser(
        description=
        'Given a mixtape and a list of change operations, output a file with the expected changes.')

    # arguments are positional
    parser.add_argument('mixtape_json')
    parser.add_argument('changes_json')
    parser.add_argument('output_json')

    args = parser.parse_args()

    if not path.exists(args.mixtape_json):
        raise FileNotFoundError('Please provide the name and path to the mixtape (eg., mixtape.json).')
    if not path.exists(args.changes_json):
        raise FileNotFoundError('Please provide the name and path to the changes (eg., changes.json).')

    mixtape_json = json.load(open(args.mixtape_json, 'r'))
    changes_json = json.load(open(args.changes_json, 'r'))

    super_mixer = SuperMixer(mixtape_json, changes_json)
    results = super_mixer.run()

    # save results
    data_to_save = json.dumps(results, indent=4, cls=UUIDEncoder)

    with open(args.output_json, "w") as f:
        f.write(data_to_save)

    logging.info("*** Program Complete")
