using System;
using Google.Apis.Auth.OAuth2;
using Google.Apis.Gmail.v1;
using Google.Apis.Gmail.v1.Data;
using Google.Apis.Services;
using Google.Apis.Util.Store;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace mgmcrimereader
{

    class Program
    { // If modifying these scopes, delete your previously saved credentials
        // at ~/.credentials/gmail-dotnet-quickstart.json
        static string[] Scopes = { GmailService.Scope.GmailReadonly };
        static string ApplicationName = "Gmail API .NET Quickstart";
        private string DecodeURLEncodedBase64EncodedString(string sInput)
        {
            string sBase46codedBody = sInput.Replace("-", "+").Replace("_", "/").Replace("=", String.Empty);  //get rid of URL encoding, and pull any current padding off.
            string sPaddedBase46codedBody = sBase46codedBody.PadRight(sBase46codedBody.Length + (4 - sBase46codedBody.Length % 4) % 4, '=');  //re-pad the string so it is correct length.
            byte[] data = Convert.FromBase64String(sPaddedBase46codedBody);
            return Encoding.UTF8.GetString(data);
        }
        static void Main(string[] args)
        {
            UserCredential credential;

            using (var stream =
                new FileStream("credentials.json", FileMode.Open, FileAccess.Read))
            {
                // The file token.json stores the user's access and refresh tokens, and is created
                // automatically when the authorization flow completes for the first time.
                string credPath = "token.json";
                credential = GoogleWebAuthorizationBroker.AuthorizeAsync(
                    GoogleClientSecrets.Load(stream).Secrets,
                    Scopes,
                    "user",
                    CancellationToken.None,
                    new FileDataStore(credPath, true)).Result;
                Console.WriteLine("Credential file saved to: " + credPath);
            }

            // Create Gmail API service.
            var service = new GmailService(new BaseClientService.Initializer()
            {
                HttpClientInitializer = credential,
                ApplicationName = ApplicationName,

            });

            // Define parameters of request.
            UsersResource.MessagesResource.ListRequest request = service.Users.Messages.List("me");

            //request.LabelIds = 
            //Google.Apis.Util.Repeatable<string> foo = new Google.Apis.Util.Repeatable<string>(new List<string>());
            //request.LabelIds = foo;
            //request.LabelIds.Append<string>("crimedata");
            // List messages.
            
            IList<Message> messages = request.Execute().Messages;
            Console.WriteLine("messages:");
            if (messages != null && messages.Count > 0)
            {
                foreach (var messageItem in messages)
                {
                    Google.Apis.Gmail.v1.UsersResource.MessagesResource.GetRequest t = service.Users.Messages.Get("me", messageItem.Id);
                    //t.Format = UsersResource.MessagesResource.GetRequest.FormatEnum.Raw;
                    Google.Apis.Gmail.v1.Data.Message m = t.Execute();

                    foreach (var head1 in m.Payload.Headers)
                    {
                        if (head1.Name.Equals("Subject"))
                            Console.WriteLine("{0}", head1.Value);
                    }
                }
            }
            else
            {
                Console.WriteLine("No messages found.");
            }
            Console.WriteLine("Continue");
            Console.Read();
        }
    }


}
