using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Windows;
using Newtonsoft.Json;
using Microsoft.WindowsAPICodePack.Dialogs;
using System.Windows.Controls;
using System.ComponentModel;
using System.Windows.Data;

namespace WPF_Test
{
    /// <summary>
    /// MainWindow.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class MainWindow : Window
    {
        List<VMListClass> vm_list;
        public MainWindow()
        {
            InitializeComponent();
            ApiClient client = ApiClient.getInstance();
            // Get VM list
            string result = client.getVMList();
            if (result == null) MessageBox.Show("서버 목록을 가져오지 못했습니다.", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            else
            {
                //Create List
                dynamic obj = JsonConvert.DeserializeObject(result);
                vm_list = new List<VMListClass>();
                foreach (var item in obj)
                {
                    vm_list.Add(new VMListClass() { node_name = item.node_name, ip_addr = item.ip_addr, last_updated = item.updated_time });
                }

                // Binding List
                lvVMList.ItemsSource = vm_list;
            }
        }

        async private void change_mac_addr_btn_Click(object sender, RoutedEventArgs e)
        {
            List<string> node_name_list = getCheckedNodeNameList(vm_list);
            if (node_name_list.Count != 0)
            {
                MessageBoxResult result = MessageBox.Show("MAC Address의 변경은 서버의 재부팅을 필요로 합니다.\n계속하시겠습니까?", "경고", MessageBoxButton.YesNo, MessageBoxImage.Warning);
                if (result == MessageBoxResult.Yes)
                {
                    ProgressWindow progressWindow = new ProgressWindow();
                    progressWindow.Title = "MAC Address 변경 진행중...";
                    progressWindow.ProgressBar.Maximum = node_name_list.Count;
                    progressWindow.Btn_OK.IsEnabled = false;
                    progressWindow.Show();
                    //Disable main window
                    App.Current.MainWindow.IsEnabled = false;

                    ApiClient client = ApiClient.getInstance();
                    //Before using ProgressWindowVariable, clean it
                    ProgressWindowVariables.result_listbox.Clear();
                    //Run it Async!
                    foreach (string item in node_name_list)
                    {
                        ApiClient.Response response = await client.changeVMMacAddr(item);
                        ResponseListClass _response = new ResponseListClass { node_name = item, message = response.message, response_code = response.response_code };
                        progressWindow.lv_Result.Items.Add(_response);
                        progressWindow.ProgressBar.Value++;
                    }
                    progressWindow.Btn_OK.IsEnabled = true;
                    App.Current.MainWindow.IsEnabled = true;
                }
            }

            else MessageBox.Show("선택된 서버가 없습니다.", "오류", MessageBoxButton.OK, MessageBoxImage.Error);

        }
        async private void Allocate_SOCKS_Btn_Click(object sender, RoutedEventArgs e)
        {
            List<string> node_name_list = getCheckedNodeNameList(vm_list);
            if (node_name_list.Count == 0)
            {
                MessageBox.Show("선택된 서버가 없습니다.", "오류", MessageBoxButton.OK, MessageBoxImage.Error);
                return;
            }

            //Before open window, clear SOCKS ID/PW Properties
            App.Current.Properties["SOCKS_username"] = null;
            App.Current.Properties["SOCKS_password"] = null;
            App.Current.Properties["SOCKS_period"] = null;
            //Open window
            SOCKSUserWindow socksuserWindow = new SOCKSUserWindow();
            socksuserWindow.ShowDialog();
            //Check Properties
            if ((App.Current.Properties["SOCKS_username"] != null) && (App.Current.Properties["SOCKS_password"] != null) && (App.Current.Properties["SOCKS_period"] != null))
            {
                ProgressWindow progressWindow = new ProgressWindow();
                progressWindow.Title = "SOCKS/OVPN 계정 할당중...";
                progressWindow.ProgressBar.Maximum = node_name_list.Count;
                progressWindow.Btn_OK.IsEnabled = false;
                progressWindow.Show();
                //Disable main window
                App.Current.MainWindow.IsEnabled = false;

                ApiClient client = ApiClient.getInstance();
                //Before using ProgressWindowVariable, clean it
                ProgressWindowVariables.result_listbox.Clear();
                //Run it Async!
                foreach (string item in node_name_list)
                {
                    ApiClient.Response response = await client.setSOCKSAccount(item);
                    ResponseListClass _response = new ResponseListClass { node_name = item, message = response.message, response_code = response.response_code };
                    progressWindow.lv_Result.Items.Add(_response);
                    progressWindow.ProgressBar.Value++;
                }
                //Enable btn and MainWindow
                progressWindow.Btn_OK.IsEnabled = true;
                App.Current.MainWindow.IsEnabled = true;
            }
            else MessageBox.Show("취소되었습니다.", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
        }

        private void SOCKSLeaseListBtn_Click(object sender, RoutedEventArgs e)
        {
            SOCKSLeaseListWindow socks_lease_listWindow = new SOCKSLeaseListWindow();
            socks_lease_listWindow.Show();
        }

        public List<string> getCheckedNodeNameList(List<VMListClass> vm_list)
        {
            List<string> checked_list = new List<string>();
            foreach (var item in vm_list)
            {
                if (item.IsChecked == true) checked_list.Add(item.node_name);
            }
            return checked_list;
        }
        private void Refresh_Btn_Click(object sender, RoutedEventArgs e)
        {
            this.Refresh_Btn.IsEnabled = false;
            //Disable main window
            App.Current.MainWindow.IsEnabled = false;
            ApiClient client = ApiClient.getInstance();
            // Get VM list
            string result = client.getVMList();
            if (result == null) MessageBox.Show("서버 목록을 가져오지 못했습니다.", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            else
            {
                //Create List
                dynamic obj = JsonConvert.DeserializeObject(result);
                vm_list.Clear();
                foreach (var item in obj)
                {
                    vm_list.Add(new VMListClass() { node_name = item.node_name, ip_addr = item.ip_addr, last_updated = item.updated_time });
                }
                lvVMList.Items.Refresh();
            }
            this.Refresh_Btn.IsEnabled = true;
            App.Current.MainWindow.IsEnabled = true;
        }
        async private void GetOVPNProfileBtn_Click(object sender, RoutedEventArgs e)
        {
            // Validate checked vm list
            List<string> node_name_list = getCheckedNodeNameList(vm_list);
            if (node_name_list.Count == 0)
            {
                MessageBox.Show("선택된 서버가 없습니다.", "오류", MessageBoxButton.OK, MessageBoxImage.Error);
                return;
            }

            var dlg = new CommonOpenFileDialog();
            dlg.Title = "OVPN 프로파일을 저장할 폴더를 지정하십시오.";
            dlg.IsFolderPicker = true;

            dlg.AddToMostRecentlyUsedList = false;
            dlg.AllowNonFileSystemItems = false;
            dlg.EnsureFileExists = true;
            dlg.EnsurePathExists = true;
            dlg.EnsureReadOnly = false;
            dlg.EnsureValidNames = true;
            dlg.Multiselect = false;
            dlg.ShowPlacesList = true;

            if (dlg.ShowDialog() == CommonFileDialogResult.Ok)
            {
                string folder = dlg.FileName;
                // TODO: Before start, validate permission
                //Disable main window
                App.Current.MainWindow.IsEnabled = false;
                //Open window
                ProgressWindow progressWindow = new ProgressWindow();
                progressWindow.Title = "OVPN 프로파일 저장중...";
                progressWindow.ProgressBar.Maximum = node_name_list.Count;
                progressWindow.Btn_OK.IsEnabled = false;
                progressWindow.Show();

                ApiClient client = ApiClient.getInstance();
                //Before using ProgressWindowVariable, clean it
                ProgressWindowVariables.result_listbox.Clear();
                //Run it Async!
                foreach (string item in node_name_list)
                {
                    ApiClient.Response response = await client.getOVPNProfile(item);
                    ResponseListClass _response = new ResponseListClass { node_name = item, message = response.message, response_code = response.response_code };
                    progressWindow.lv_Result.Items.Add(_response);
                    progressWindow.ProgressBar.Value++;

                    //Parse response.data to JSON
                    dynamic obj = JsonConvert.DeserializeObject<Dictionary<string, string>>(response.data);

                    /* Save OVPN Profile */
                    //Find IP Address from node_name
                    VMListClass result = vm_list.Find(x => x.node_name == obj["node_name"]);
                    string IpAddr = result.ip_addr;
                    DateTime dateTime = Convert.ToDateTime(obj["updated_time"]);
                    string updated_time = dateTime.ToString("yyyy-MM-dd");
                    string profilePath = Path.Combine(folder, obj["node_name"] + "-" + IpAddr + "-" + updated_time + ".ovpn");
                    byte[] decoded_profile_b64 = Convert.FromBase64String(obj["cert_key"]);
                    string decoded_profile_str = System.Text.Encoding.UTF8.GetString(decoded_profile_b64);
                    using (StreamWriter outputFile = new StreamWriter(profilePath))
                    {
                        outputFile.Write(decoded_profile_str);
                    }

                }
                //Enable btn and MainWindow
                progressWindow.Btn_OK.IsEnabled = true;
                App.Current.MainWindow.IsEnabled = true;
            }
            else MessageBox.Show("취소되었습니다.", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
        }


        /* Sort by click header */
        GridViewColumnHeader _lastHeaderClicked = null;
        ListSortDirection _lastDirection = ListSortDirection.Ascending;

        void GridViewColumnHeaderClickedHandler(object sender, RoutedEventArgs e)
        {
            var headerClicked = e.OriginalSource as GridViewColumnHeader;
            ListSortDirection direction;

            if (headerClicked != null)
            {
                if (headerClicked.Role != GridViewColumnHeaderRole.Padding)
                {
                    if (headerClicked != _lastHeaderClicked)
                    {
                        direction = ListSortDirection.Ascending;
                    }
                    else
                    {
                        if (_lastDirection == ListSortDirection.Ascending)
                        {
                            direction = ListSortDirection.Descending;
                        }
                        else
                        {
                            direction = ListSortDirection.Ascending;
                        }
                    }

                    var columnBinding = headerClicked.Column.DisplayMemberBinding as Binding;
                    var sortBy = columnBinding?.Path.Path ?? headerClicked.Column.Header as string;

                    Sort(sortBy, direction);

                    if (direction == ListSortDirection.Ascending)
                    {
                        headerClicked.Column.HeaderTemplate =
                          Resources["HeaderTemplateArrowUp"] as DataTemplate;
                    }
                    else
                    {
                        headerClicked.Column.HeaderTemplate =
                          Resources["HeaderTemplateArrowDown"] as DataTemplate;
                    }

                    // Remove arrow from previously sorted header
                    if (_lastHeaderClicked != null && _lastHeaderClicked != headerClicked)
                    {
                        _lastHeaderClicked.Column.HeaderTemplate = null;
                    }

                    _lastHeaderClicked = headerClicked;
                    _lastDirection = direction;
                }
            }
        }

        private void Sort(string sortBy, ListSortDirection direction)
        {
            ICollectionView dataView =
              CollectionViewSource.GetDefaultView(lvVMList.ItemsSource);

            dataView.SortDescriptions.Clear();
            SortDescription sd = new SortDescription(sortBy, direction);
            dataView.SortDescriptions.Add(sd);
            dataView.Refresh();
        }

        /* Data Structures */
        public class VMListClass
        {
            public string node_name { get; set; }
            public string ip_addr { get; set; }
            public DateTime last_updated { get; set; }
            public bool IsChecked { get; set; }
        }

        public class ResponseListClass
        {
            public string node_name { get; set; }
            public int response_code { get; set; }
            public string message { get; set; }
        }

    }
}