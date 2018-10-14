/*
 * PhttpClient.java:Webサーバにリクエストを送り、デフォルトページを受信するクライアント
 */

import java.io.*;
import java.net.*;
import java.lang.Object.*;

public class PhttpClient {
public static void main(String args[]) {
	String url = args[0];
	String host = "localhost";
	String path = "/";
	int PORT = Integer.parseInt(args[1]);

	if (args.length > 0) {
		url = args[0];
	} else {
		url = "http://" + host + ":" + PORT + path;
	}
			


try {
	//ソケット生成
	Socket socket = new Socket(host, PORT);
	BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
	BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));

	// webサーバ－へリクエスト送信
	writer.write("GET "+ url +" HTTP/1.1\r\n");
	writer.write("Host: " + host + "\r\n");
	writer.write("Connection: close\r\n");
	writer.write("\r\n");
	writer.flush();
			
	// デフォルトページを受信
	String line;
	while ((line = reader.readLine()) != null) {
		System.out.println(line);
	}
			
	writer.close();
	reader.close();
	socket.close();
	} catch (UnknownHostException e) {
         		System.err.println("Host not found");
           	System.exit(-1);
         } catch (SocketException e) {
           	System.err.println("Socket error");
           	System.exit(-1);
         } catch (IOException e) {
           	System.err.println("IO error");
           	System.exit(-1);
        }
    }
}
