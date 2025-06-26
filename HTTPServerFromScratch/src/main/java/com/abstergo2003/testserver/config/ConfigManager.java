package com.abstergo2003.testserver.config;

import com.abstergo2003.testserver.util.Json;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

public class ConfigManager {
    private static ConfigManager myConfigManager;
    private static Configuration myCurrentConfig;
    private ConfigManager() {

    }
    public static ConfigManager getInstance() {
        if (myConfigManager==null) {
            myConfigManager = new ConfigManager();
        }
        return myConfigManager;
    }

    public void loadConfigFile(String filePath) {
        FileReader fileReader = null;
        try {
            fileReader = new FileReader(filePath);
        } catch (FileNotFoundException e) {
            throw new HttpConfigurationExcpetion(e);
        }
        StringBuffer sb = new StringBuffer();
        int i;
        while(true) {
            try {
                if (!((i = fileReader.read()) != -1)) break;
            } catch (IOException e) {
                throw new HttpConfigurationExcpetion(e);
            }
            sb.append((char)i);
        }
        JsonNode conf = null;
        try {
            conf = Json.parse(sb.toString());
        } catch (JsonProcessingException e) {
            throw new HttpConfigurationExcpetion("Error parsing teh config file.");
        }
        try {
            myCurrentConfig = Json.fromJson(conf, Configuration.class);
        } catch (JsonProcessingException e) {
            throw new HttpConfigurationExcpetion("Error parsing the config file internal.");
        }
    }

    public Configuration getCurrentConfig() {
        if (myCurrentConfig == null) {
            throw new HttpConfigurationExcpetion("No current configuration set.");
        }
        return myCurrentConfig;
    }
}
