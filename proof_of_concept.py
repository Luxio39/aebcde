#!/usr/bin/python3

from pathlib import Path
import subprocess
import re


class Extractor:

    def __init__(self, target_path=Path.cwd(), drive_sample_offset='0'):
        self.target_path = target_path
        self.drive_sample_offset = drive_sample_offset

    def ripDisc(self):
        pcm_directory = self.target_path / 'pcm'
        pcm_directory.mkdir(parents=True, exist_ok=True)
        process_cdparanoia = subprocess.Popen(['cdparanoia', '-r', '-z', '-O', self.drive_sample_offset, '-B', '1-', './'], cwd=pcm_directory)
#        while process_cdparanoia.poll() == None:
#            time.sleep(2)
        process_cdparanoia.wait()
        if process_cdparanoia.returncode != 0:
            raise Exception('something seems to have gone wrong while extracting the cd audio!')

    def pcmToflac(self):
        pcm_directory = self.target_path / 'pcm'
        flac_directory = self.target_path / 'flac'
        flac_directory.mkdir(parents=True, exist_ok=True)
        for track in pcm_directory.glob('*.raw'):
            track_number = re.findall(r'\d+', str(track))[-1].zfill(2)
            process_flac = subprocess.Popen(['flac', '-o', '{}.flac'.format(track_number), '-V', '--force-raw-format', '--endian', 'little', '--sign', 'signed', '--channels', '2', '--bps', '16', '--sample-rate', '44100', track], cwd=self.target_path)
            process_flac.wait()
            if process_flac.returncode != 0:
                raise Exception('something seems to have gone wrong while encoding the pcm into flac!')

print('enter artist name: ')
artist = input()
print('enter album name: ')
album = input()
album_path = Path.cwd() / artist / album


ding = Extractor(target_path=album_path, drive_sample_offset='+6')
print('starting cdda extraction')
#ding.ripDisc()
print('starting flac encoding')
ding.pcmToflac()