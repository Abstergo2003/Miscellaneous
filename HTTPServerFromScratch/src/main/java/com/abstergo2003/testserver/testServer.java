package com.abstergo2003.testserver;


import com.abstergo2003.testserver.config.ConfigManager;
import com.abstergo2003.testserver.config.Configuration;
import com.abstergo2003.testserver.core.ServerListenerThread;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


import java.io.IOException;

public class testServer {

    private final static Logger LOGGER = LoggerFactory.getLogger(testServer.class);

    public static void main(String[] args) {

        LOGGER.info("Server Starting...");
        ConfigManager.getInstance().loadConfigFile("http.json");
        Configuration conf = ConfigManager.getInstance().getCurrentConfig();
        LOGGER.info("Using Port: " + conf.getPort());
        LOGGER.info("Using Webroot: " + conf.getWebroot());

        try {
            ServerListenerThread serverListenerThread = new ServerListenerThread(conf.getWebroot(), conf.getPort());
            serverListenerThread.start();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
