package com.friday.rpg;

import com.friday.rpg.ui.GameWindow;
import javafx.application.Application;
import javafx.stage.Stage;

public class Main extends Application {
    public static void main(String[] args) {
        launch(args);
    }
    
    @Override
    public void start(Stage primaryStage) {
        GameWindow gameWindow = new GameWindow();
        gameWindow.initialize(primaryStage);
    }
}
