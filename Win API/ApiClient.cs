using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using RestSharp;
using RestSharp.Authenticators;
using Newtonsoft.Json;

namespace WPF_Test
{
    class ApiClient
    {
        public string auth_key = null;
        private static ApiClient _client;
        private RestClient client;
        //Singleton Initializer
        private ApiClient()
        {
           client = new RestClient("http://cemcom2.codns.com:2095");

        }
        public static ApiClient getInstance()
        {
            if (_client == null) _client = new ApiClient();
            return _client;
        }

        public void getAuthorization(string username, string password)
        {
            //Create header
            var request = new RestRequest("/auth/", Method.POST);
            request.RequestFormat = DataFormat.Json;
            request.AddBody(new { username = username, password = password });

            var response = client.Execute(request);
            if ((int)response.StatusCode == 200)
            {
                var obj = JsonConvert.DeserializeObject<dynamic>(response.Content);
                auth_key = obj.Authorization;
            }
            // if failed, set auth_key to null
            else auth_key = null;
        }

        public string getVMList()
        {
            var request = new RestRequest("/node/", Method.GET);
            request.RequestFormat = DataFormat.Json;
            request.AddHeader("Authorization", auth_key);

            var response = client.Execute(request);

            if ((int)response.StatusCode == 200) return response.Content.ToString();
            else if ((int)response.StatusCode == 401)
            {
                //Re-authentication
                this.getAuthorization((string)App.Current.Properties["username"], (string)App.Current.Properties["password"]);
                //Recursion
                string result = this.getVMList();
                return result;
            }
            else return null;
        }
        public string getSOCKSLeaseList()
        {
            var request = new RestRequest("/lease/", Method.GET);
            request.RequestFormat = DataFormat.Json;
            request.AddHeader("Authorization", auth_key);

            var response = client.Execute(request);

            if ((int)response.StatusCode == 200) return response.Content.ToString();
            else if ((int)response.StatusCode == 401)
            {
                //Re-authentication
                this.getAuthorization((string)App.Current.Properties["username"], (string)App.Current.Properties["password"]);
                //Recursion
                string result = this.getSOCKSLeaseList();
                return result;
            }
            else return null;
        }
        async public Task<Response> getOVPNProfile(string node_name)
        {
            var request = new RestRequest("/node/cert/", Method.GET);
            request.RequestFormat = DataFormat.Json;
            request.AddHeader("Authorization", auth_key);
            request.AddParameter("node_name", node_name);

            var response = await client.ExecuteAsync(request);
            
            Response _response = new Response();

            if ((int)response.StatusCode == 401)
            {
                //Re-authentication
                this.getAuthorization((string)App.Current.Properties["username"], (string)App.Current.Properties["password"]);
                response = client.Execute(request);
            }

            else if((int)response.StatusCode == 200)
            {
                _response.data = response.Content.ToString();
                _response.message = node_name + " OVPN Profile is successfully downloaded.";
                _response.response_code = (int)response.StatusCode;
            }

            else
            {
                _response.message = response.Content.ToString();
                _response.response_code = (int)response.StatusCode;
            }
            return _response;
        }

        async public Task<Response> changeVMMacAddr(string node_name)
        {
            var request = new RestRequest("/node/mac/", Method.POST);
            request.RequestFormat = DataFormat.Json;
            request.AddBody(new { node_name = node_name, Authorization = auth_key });

            var response = await client.ExecuteAsync(request);
            //If fail to authentication
            if ((int)response.StatusCode == 401)
            {
                //Re-authentication
                this.getAuthorization((string)App.Current.Properties["username"], (string)App.Current.Properties["password"]);
                response = client.Execute(request);
            }
            //else
            Response _response = new Response();
            _response.message = response.Content.ToString();
            _response.response_code = (int)response.StatusCode;

            return _response;
        }
        async public Task<Response> setSOCKSAccount(string node_name)
        {
            var request = new RestRequest("/lease/", Method.POST);
            request.RequestFormat = DataFormat.Json;
            request.AddBody(new
            {
                node_name = node_name,
                Authorization = auth_key,
                username = App.Current.Properties["SOCKS_username"],
                password = App.Current.Properties["SOCKS_password"],
                period = int.Parse(App.Current.Properties["SOCKS_period"].ToString())
            });

            var response = await client.ExecuteAsync(request);
            //If fail to authentication
            if ((int)response.StatusCode == 401)
            {
                //Re-authentication
                this.getAuthorization((string)App.Current.Properties["username"], (string)App.Current.Properties["password"]);
                response = client.Execute(request);
            }
            //else
            Response _response = new Response();
            _response.message = response.Content.ToString();
            _response.response_code = (int)response.StatusCode;

            return _response;
        }

        async public Task<Response> removeSOCKSLeaseAccount(string node_name, string username)
        {
            var request = new RestRequest("/lease/", Method.DELETE);
            request.RequestFormat = DataFormat.Json;
            request.AddBody(new { node_name = node_name, username = username, Authorization = auth_key });

            var response = await client.ExecuteAsync(request);
            //If fail to authentication
            if ((int)response.StatusCode == 401)
            {
                //Re-authentication
                this.getAuthorization((string)App.Current.Properties["username"], (string)App.Current.Properties["password"]);
                response = client.Execute(request);
            }
            //else
            Response _response = new Response();
            _response.message = response.Content.ToString();
            _response.response_code = (int)response.StatusCode;

            return _response;
        }

        public class Response
        {
            public int response_code { get; set; }
            public string message { get; set; }
            public string data { get; set; }
        }
    }
}
