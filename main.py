import wx
import threading
from moviepy.editor import VideoFileClip
import os

# Uyumlu format dönüşümleri
compatible_formats = {
    'mov': ['mp4', 'avi', 'mkv', 'flv'],
    'mp4': ['mov', 'avi', 'mkv', 'flv'],
    'avi': ['mov', 'mp4', 'mkv', 'flv'],
    'mkv': ['mov', 'mp4', 'avi', 'flv'],
    'flv': ['mov', 'mp4', 'avi', 'mkv']
}

class VideoConverterFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Video Converter', size=(500, 200))
        panel = wx.Panel(self)
        
        # GridBagSizer oluşturma
        main_sizer = wx.GridBagSizer(vgap=10, hgap=10)

        # Uzantı seçimi için ComboBox
        format_label = wx.StaticText(panel, label='Convert To:')
        main_sizer.Add(format_label, pos=(0, 0), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.ALL, border=5)
        self.format_combo = wx.ComboBox(panel, choices=['mp4', 'avi', 'mkv', 'flv'], style=wx.CB_DROPDOWN)
        main_sizer.Add(self.format_combo, pos=(0, 1), flag=wx.EXPAND|wx.ALL, border=5)

        # Video dosyası seçme
        file_picker_label = wx.StaticText(panel, label='Select Video File:')
        main_sizer.Add(file_picker_label, pos=(1, 0), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.ALL, border=5)
        self.file_picker = wx.FilePickerCtrl(panel, wildcard="Video files (*.mov;*.mp4;*.avi;*.mkv;*.flv)|*.mov;*.mp4;*.avi;*.mkv;*.flv")
        main_sizer.Add(self.file_picker, pos=(1, 1), span=(1, 2), flag=wx.EXPAND|wx.ALL, border=5)

        # Dönüştürme butonu
        convert_button = wx.Button(panel, label='Convert')
        main_sizer.Add(convert_button, pos=(2, 1), span=(1, 1), flag=wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, border=5)
        convert_button.Bind(wx.EVT_BUTTON, self.on_convert)

        # İlerleme durumu için StaticText
        self.progress_text = wx.StaticText(panel, label='')
        main_sizer.Add(self.progress_text, pos=(3, 0), span=(1, 3), flag=wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, border=5)

        panel.SetSizerAndFit(main_sizer)
        self.Show()

    def on_convert(self, event):
        file_path = self.file_picker.GetPath()
        selected_format = self.format_combo.GetValue()

        if not file_path:
            wx.MessageBox('Please select a video file.', 'Error', wx.OK | wx.ICON_ERROR)
            return

        # Dosya uzantısını kontrol etme
        _, file_extension = os.path.splitext(file_path)
        file_extension = file_extension[1:].lower()  # "." işaretini kaldır ve küçük harfe çevir

        if file_extension not in compatible_formats:
            wx.MessageBox('Selected file format is not supported.', 'Error', wx.OK | wx.ICON_ERROR)
            return

        if selected_format not in compatible_formats[file_extension]:
            wx.MessageBox(f'File cannot be converted to {selected_format}.', 'Error', wx.OK | wx.ICON_ERROR)
            return

        # Dönüşüm işlemini başlat
        self.start_conversion(file_path, selected_format)

    def start_conversion(self, file_path, selected_format):
        # Dönüşüm işlemini başlatmadan önce ilerleme durumunu göster
        self.progress_text.SetLabel('Conversion in progress...')

        def conversion_thread():
            try:
                base_name, _ = os.path.splitext(file_path)
                output_file_path = f"{base_name}.{selected_format}"

                clip = VideoFileClip(file_path)
                clip.write_videofile(output_file_path, codec='libx264')

                wx.CallAfter(self.progress_text.SetLabel, f'Conversion completed! File path: {output_file_path}')
            except Exception as e:
                wx.CallAfter(wx.MessageBox, f'An error occurred during conversion:\n{str(e)}', 'Error', wx.OK | wx.ICON_ERROR)
                wx.CallAfter(self.progress_text.SetLabel, 'Conversion failed.')

        # Dönüşüm işlemini başlat (thread)
        threading.Thread(target=conversion_thread).start()

if __name__ == '__main__':
    app = wx.App(False)
    frame = VideoConverterFrame()
    app.MainLoop()
