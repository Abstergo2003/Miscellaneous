package com.abstergo2003.testserver.util;

import com.abstergo2003.http.ContentType;
import com.abstergo2003.testserver.config.ConfigManager;
import com.abstergo2003.testserver.config.Configuration;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class FileHandler {
    public static void write(String filePath, String content) throws IOException {
        Path path = Paths.get(filePath);
        byte[] contentBytes = content.getBytes();
        Files.write(path, contentBytes);
    }
    public static String parsePath(String target) {
        char lastChar = target.charAt(target.length() - 1);
        //ConfigManager.getInstance().loadConfigFile("src/main/resources/http.json");
        Configuration conf = ConfigManager.getInstance().getCurrentConfig();
        String folder = conf.getWebroot();
        if (lastChar == '/') {
            return "C:\\manga server\\" + folder + target + "index.html";
        } else {
            return "C:\\manga server\\public" + target;
        }
    }
    public static ContentType getContentType(String target) {
        String filePath = parsePath(target);
        return ContentType.matchContentType(filePath);
    }
    public static byte[] readFile(String filePath) throws IOException {
        File file = new File(filePath);
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        try (FileInputStream inputStream = new FileInputStream(file)) {
            byte[] buffer = new byte[1024];
            int bytesRead;
            while ((bytesRead = inputStream.read(buffer)) != -1) {
                outputStream.write(buffer, 0, bytesRead);
            }
        }
        return outputStream.toByteArray();
    }
}