package xml;
import java.io.*;
import java.net.*;

public class XmlHttpRequest {
    public static void main(String[] args) throws Exception {
        URL url = new URL("https://www.w3schools.com/xml/note.xml");

        // Open a connection to the server
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();

        // Set the request method to GET and the content type to XML
        conn.setRequestMethod("GET");
        conn.setRequestProperty("Content-Type", "application/xml");

        // Read the XML response from the server
        BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
        StringBuilder response = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            response.append(line + "\n");
        }
        reader.close();

        System.out.println(response.toString());
    }
}
