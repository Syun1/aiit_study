/*
 * OriginalServer.java:2つの整数を受信し、最大公約数を求めるサーバ
 */
import java.io.*;
import java.net.*;
import java.util.*;

public class OriginalServer {
    public static void main (String args[]) {
        try{                                
        	//ソケット生成
        	int PORT = Integer.parseInt(args[0]);
            ServerSocket serverSocket = new ServerSocket(PORT);

            //入出力ストリームを用意し、クライアントからの要求を待つ
            Socket socket = serverSocket.accept();
            DataInputStream reader = new DataInputStream(socket.getInputStream());
            DataOutputStream writer = new DataOutputStream(socket.getOutputStream());
        	
        	// クライアントから2つの整数を受信し、出力
        	int a = reader.readInt();
          int b = reader.readInt();
        	System.out.println("整数："+a+","+b);
        	
        	// 最大公約数を求める（ユークリッドの互除法）
        	int tmp, c;
        	if(a < b) {
        		tmp = a;
        		a = b;
        		b = tmp;
        	}
        	
            c = a % b;
        	while(c != 0) {
        		a = b;
        		b = c;
        		c = a % b;
        	}
        	// 最大公約数を出力
        	System.out.println("最大公約数："+b);
        	
        	// 最大公約数をクライアントに送る
            writer.writeInt(b);
            
        	// ソケットを閉じる
        	writer.close();
            reader.close();
            socket.close();
            serverSocket.close();
        } catch (SocketException e)
            {
                System.err.println("Socket error");
                System.exit(-1);
            } catch (IOException e) {
            System.err.println("IO error");
            System.exit(-1);
        }
    }
}
