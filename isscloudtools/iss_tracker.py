
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import uic, QtCore
from isscloudtools._resources import resource_filename
from glob import glob
import os
from historydict import HistoryDict

from .initialize import get_gdrive_service
from .gdrive import folder_exists_in_root, create_folder, folder_exists, upload_file

ui_path = resource_filename('ui/Tracker.ui')

class ISSTracker(*uic.loadUiType(ui_path)):


    def __init__(self,
                 RE=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.RE = RE
        self.setWindowTitle('ISS Folder Tracking')
        self.addCanvas()
        self.timer_update_user_info = QtCore.QTimer()
        self.timer_update_user_info.timeout.connect(self.check_folder)
        self.timer_update_user_info.start(20 * 1000)
        self.service = get_gdrive_service()
        self.reset_metadata()
        self.tracking = False
        self.push_track.clicked.connect(self.track_push_manager)
        self.push_reset_metadata.clicked.connect(self.reset_metadata)
        self.push_move_all.clicked.connect(self.push_all)


    def reset_metadata(self):
        ROOT_PATH = '/nsls2/xf08id'
        USER_FILEPATH = 'users'
        self.RE.md = HistoryDict('/nsls2/xf08id/metadata/bluesky_history.db')
        self.year = self.RE.md['year']
        self.cycle = self.RE.md['cycle']
        self.proposal = self.RE.md['PROPOSAL']
        self.folder = f"{ROOT_PATH}/{USER_FILEPATH}/{self.year}/{self.cycle}/{self.proposal}/"
        self.folder_list = glob(f'{self.folder}*.dat')
        self.label_metadata.setText(f'Year: {self.year} Cycle: {self.cycle} Proposal: {self.proposal}')
        self.set_location()



    def set_location(self):
        year_folder = folder_exists_in_root(self.service, self.year)
        if year_folder is None:
            print('creating')
            year_folder = create_folder(self.service,folder_name=self.year)

        cycle_folder = folder_exists(self.service, parent=year_folder, folder_name = self.cycle)
        if cycle_folder is None:
            print('creating')
            cycle_folder = create_folder(self.service,parent=year_folder, folder_name = self.cycle)

        proposal_folder = folder_exists(self.service, parent=cycle_folder, folder_name=self.proposal)
        if proposal_folder is None:
            print('creating')
            proposal_folder = create_folder(self.service,parent=cycle_folder, folder_name = self.proposal)

        self.location = proposal_folder


    def close_app(self):
        self.close()

    def addCanvas(self):
        self.figureBinned = Figure()
        self.figureBinned.set_facecolor(color='#FcF9F6')
        self.figureBinned.ax = self.figureBinned.add_subplot(111)
        self.canvas = FigureCanvas(self.figureBinned)

    def check_folder(self):
        if self.tracking is True:
            self.new_folder_list = glob(f'{self.folder}*.dat')
            print(f'Now {len(self.new_folder_list)}')
            new_files = list(set(self.new_folder_list) - set(self.folder_list))
            if new_files!=[]:
                self.folder_list = self.new_folder_list
                for file in new_files:
                    print(f'New file found {file}')
                    upload_file(self.service, parent=self.location, file_name=os.path.basename(file), from_local_file = file)
            else:
                print('nooooooo')

    def track_push_manager(self):
        self.tracking = self.push_track.isChecked()

    def push_all(self):
        files = glob(f'{self.folder}*.dat')
        for file in files:
            print(f'New file found {file}')
            upload_file(self.service, parent=self.location, file_name=os.path.basename(file), from_local_file=file)























