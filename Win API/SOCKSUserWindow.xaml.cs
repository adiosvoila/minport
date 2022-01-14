using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;

namespace WPF_Test
{
    /// <summary>
    /// SOCKSUserWindow.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class SOCKSUserWindow : Window
    {
        public SOCKSUserWindow()
        {
            InitializeComponent();
        }

        private void Btn_OK_Click(object sender, RoutedEventArgs e)
        {
            //Check ID/PW is Alphanumeric
            if (TextBox_Username.Text.All(char.IsLetterOrDigit) && TextBox_Password.Password.All(char.IsLetterOrDigit))
            {
                App.Current.Properties["SOCKS_username"] = TextBox_Username.Text;
                App.Current.Properties["SOCKS_password"] = TextBox_Password.Password;
                
                //Check Period is Numeric
                if (TextBox_Period.Text.All(char.IsNumber))
                {
                    App.Current.Properties["SOCKS_period"] = TextBox_Period.Text;
                }
                else MessageBox.Show("기간은 숫자만 입력할 수 있습니다.", "Error", MessageBoxButton.OK, MessageBoxImage.Error);

                //Check Password and Password_Retype is equal
                if (TextBox_Password.Password == TextBox_Password_Retype.Password) this.Close();
                else MessageBox.Show("패스워드가 서로 일치하지 않습니다.", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
            else MessageBox.Show("사용자 이름과 암호는 영문/숫자만 사용 가능합니다.", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
        }

        private void Btn_Cancel_Click(object sender, RoutedEventArgs e)
        {
            App.Current.Properties["SOCKS_username"] = null;
            App.Current.Properties["SOCKS_password"] = null;
            App.Current.Properties["SOCKS_period"] = null;
            this.Close();
        }
    }
}
