using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;

namespace WPF_Test
{
    /// <summary>
    /// LoginWindow.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class LoginWindow : Window
    {
        public LoginWindow()
        {
            InitializeComponent();
        }

        private void Btn_Login_Click(object sender, RoutedEventArgs e)
        {
            //Disable btn
            Btn_Login.IsEnabled = false;
            Btn_Cancel.IsEnabled = false;

            ApiClient client = ApiClient.getInstance();
            client.getAuthorization(TextBox_Username.Text, TextBox_Password.Password);

            //Check return
            if (client.auth_key != null)
            {
                App.Current.Properties["username"] = TextBox_Username.Text;
                App.Current.Properties["password"] = TextBox_Password.Password;
                //Open Main Window
                var mainWindow = new MainWindow();
                App.Current.MainWindow = mainWindow;
                this.Close();
                mainWindow.Show();
            }
            else MessageBox.Show("로그인 실패.\n사용자 이름과 암호를 확인하세요.", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            //Restore btn
            Btn_Login.IsEnabled = true;
            Btn_Cancel.IsEnabled = true;
        }

        private void Btn_Cancel_Click(object sender, RoutedEventArgs e)
        {
            System.Windows.Application.Current.Shutdown();
        }
    }
}
