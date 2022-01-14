using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;

namespace WPF_Test
{
    /// <summary>
    /// ProgressWindow.xaml에 대한 상호 작용 논리
    /// </summary>
    /// 
    static class ProgressWindowVariables
    {
        public static List<string> result_listbox = new List<string>();
    }
    public partial class ProgressWindow : Window
    {
        public ProgressWindow()
        {
            InitializeComponent();
            //this.Result_ListBox.ItemsSource = ProgressWindowVariables.result_listbox;
        }
        private void Btn_OK_Click(object sender, RoutedEventArgs e)
        {
            this.Close();
        }
    }
}

