/*
 * OriginalClient.java:2つの整数を引数として入力し、最大公約数をサーバーから受信するクライアント
 */

import java.io.*;
import java.net.*;

public class OriginalClient {
    public static void main (String args[]) {
    	
    	// ホスト名、ポート番号、および2つの整数を引数で指定
    	String host = args[0];
    	int PORT = Integer.parseInt(args[1]);
    	int a = (new Integer(args[2])).intValue();
    	int b = (new Integer(args[3])).intValue();
    	
        try{                                 
        	//ソケット生成
            Socket socket = new Socket(host, PORT);
            DataInputStream reader = new DataInputStream(socket.getInputStream());
            DataOutputStream writer = new DataOutputStream(socket.getOutputStream());

            // サーバへ整数を送る
        	writer.writeInt(a);
        	writer.writeInt(b);

            // サーバから最大公約数を受信し、出力
        	int GCD = reader.readInt();
        	System.out.println("最大公約数："+GCD);
        	
        	// ソケットを閉じる
            writer.close();
            reader.close();
            socket.close();
        } catch (UnknownHostException e)
            {
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
