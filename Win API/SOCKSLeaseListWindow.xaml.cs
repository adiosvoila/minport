using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;

namespace WPF_Test
{
    /// <summary>
    /// SOCKSLeaseListWindow.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class SOCKSLeaseListWindow : Window
    {
        List<SOCKSLeaseListClass> lease_list;
        public SOCKSLeaseListWindow()
        {
            InitializeComponent();
            ApiClient client = ApiClient.getInstance();
            // Get Lease list
            string result = client.getSOCKSLeaseList();
            if (result == null) MessageBox.Show("SOCKS/OVPN 임대 목록을 가져오지 못했습니다.", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            else
            {
                //Create List
                dynamic obj = JsonConvert.DeserializeObject(result);
                lease_list = new List<SOCKSLeaseListClass>();
                foreach (var item in obj)
                {
                    lease_list.Add(new SOCKSLeaseListClass() { node_name = item.node_name, username = item.username, password = item.password, expire_date = item.expire_date });
                }
                // Binding List
                lvSOCKSLeaseList.ItemsSource = lease_list;
            }
        }
        async private void RemoveLeaseBtn_Click(object sender, RoutedEventArgs e)
        {
            List<SOCKSRemoveLeaseListClass> node_list = getCheckedNodeNameList(lease_list);
            if (node_list.Count != 0)
            {
                MessageBoxResult result = MessageBox.Show("정말 삭제하시겠습니까?", "경고", MessageBoxButton.YesNo, MessageBoxImage.Warning);
                if (result == MessageBoxResult.Yes)
                {
                    ProgressWindow progressWindow = new ProgressWindow();
                    progressWindow.Title = "SOCKS/OVPN 서버 계정 삭제중...";
                    progressWindow.ProgressBar.Maximum = node_list.Count;
                    progressWindow.Btn_OK.IsEnabled = false;
                    progressWindow.Show();

                    ApiClient client = ApiClient.getInstance();
                    //Before using ProgressWindowVariable, clean it
                    ProgressWindowVariables.result_listbox.Clear();
                    //Run it Async!
                    foreach (var item in node_list)
                    {
                        ApiClient.Response response = await client.removeSOCKSLeaseAccount(item.node_name, item.username);
                        ResponseListClass _response = new ResponseListClass { node_name = item.node_name, message = response.message, response_code = response.response_code };
                        progressWindow.lv_Result.Items.Add(_response);
                        progressWindow.ProgressBar.Value++;
                    }
                    progressWindow.Btn_OK.IsEnabled = true;
                    refreshLeaseList();
                }
            }

            else MessageBox.Show("선택된 서버가 없습니다.", "오류", MessageBoxButton.OK, MessageBoxImage.Error);
        }
        private void refreshLeaseList()
        {
            //Before start, clean lease_list
            lease_list.Clear();

            ApiClient client = ApiClient.getInstance();
            // Get Lease list
            string result = client.getSOCKSLeaseList();
            if (result == null) MessageBox.Show("SOCKS 임대 목록을 가져오지 못했습니다.", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            else
            {
                //Create List
                dynamic obj = JsonConvert.DeserializeObject(result);
                foreach (var item in obj)
                {
                    lease_list.Add(new SOCKSLeaseListClass() { node_name = item.node_name, username = item.username, password = item.password, expire_date = item.expire_date });
                }
                //Update databinding
                lvSOCKSLeaseList.Items.Refresh();

            }

        }

        public List<SOCKSRemoveLeaseListClass> getCheckedNodeNameList(List<SOCKSLeaseListClass> lease_list)
        {
            List<SOCKSRemoveLeaseListClass> checked_list = new List<SOCKSRemoveLeaseListClass>();
            foreach (var item in lease_list)
            {
                if (item.IsChecked == true) checked_list.Add(new SOCKSRemoveLeaseListClass { node_name = item.node_name, username = item.username });
            }
            return checked_list;
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
              CollectionViewSource.GetDefaultView(lvSOCKSLeaseList.ItemsSource);

            dataView.SortDescriptions.Clear();
            SortDescription sd = new SortDescription(sortBy, direction);
            dataView.SortDescriptions.Add(sd);
            dataView.Refresh();
        }
    }






    /* Data Structures */
    public class SOCKSLeaseListClass
    {
        public string username { get; set; }
        public string password { get; set; }
        public string node_name { get; set; }
        public DateTime expire_date { get; set; }
        public bool IsChecked { get; set; }
    }

    public class SOCKSRemoveLeaseListClass
    {
        public string username { get; set; }
        public string node_name { get; set; }
    }

    public class ResponseListClass
    {
        public string node_name { get; set; }
        public int response_code { get; set; }
        public string message { get; set; }
    }
}
