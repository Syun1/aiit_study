/*
 * OriginalClient.java:2�̐����������Ƃ��ē��͂��A�ő���񐔂��T�[�o�[�����M����N���C�A���g
 */

import java.io.*;
import java.net.*;

public class OriginalClient {
    public static void main (String args[]) {
    	
    	// �z�X�g���A�|�[�g�ԍ��A�����2�̐����������Ŏw��
    	String host = args[0];
    	int PORT = Integer.parseInt(args[1]);
    	int a = (new Integer(args[2])).intValue();
    	int b = (new Integer(args[3])).intValue();
    	
        try{                                 
        	//�\�P�b�g����
            Socket socket = new Socket(host, PORT);
            DataInputStream reader = new DataInputStream(socket.getInputStream());
            DataOutputStream writer = new DataOutputStream(socket.getOutputStream());

            // �T�[�o�֐����𑗂�
        	writer.writeInt(a);
        	writer.writeInt(b);

            // �T�[�o����ő���񐔂���M���A�o��
        	int GCD = reader.readInt();
        	System.out.println("�ő���񐔁F"+GCD);
        	
        	// �\�P�b�g�����
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
