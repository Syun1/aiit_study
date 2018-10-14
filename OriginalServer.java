/*
 * OriginalServer.java:2�̐�������M���A�ő���񐔂����߂�T�[�o
 */
import java.io.*;
import java.net.*;
import java.util.*;

public class OriginalServer {
    public static void main (String args[]) {
        try{                                
        	//�\�P�b�g����
        	int PORT = Integer.parseInt(args[0]);
            ServerSocket serverSocket = new ServerSocket(PORT);

            //���o�̓X�g���[����p�ӂ��A�N���C�A���g����̗v����҂�
            Socket socket = serverSocket.accept();
            DataInputStream reader = new DataInputStream(socket.getInputStream());
            DataOutputStream writer = new DataOutputStream(socket.getOutputStream());
        	
        	// �N���C�A���g����2�̐�������M���A�o��
        	int a = reader.readInt();
          int b = reader.readInt();
        	System.out.println("�����F"+a+","+b);
        	
        	// �ő���񐔂����߂�i���[�N���b�h�̌ݏ��@�j
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
        	// �ő���񐔂��o��
        	System.out.println("�ő���񐔁F"+b);
        	
        	// �ő���񐔂��N���C�A���g�ɑ���
            writer.writeInt(b);
            
        	// �\�P�b�g�����
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
