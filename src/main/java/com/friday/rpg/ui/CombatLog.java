package com.friday.rpg.ui;

import javafx.scene.control.Label;
import javafx.scene.control.ScrollPane;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;

public class CombatLog extends ScrollPane {
    
    private VBox content;
    
    public CombatLog() {
        content = new VBox(2);
        content.setStyle("-fx-background-color: #0a0a0a;");
        
        setContent(content);
        setFitToWidth(true);
        setStyle("-fx-background: #0a0a0a; -fx-border-color: #1a1a1a; -fx-border-width: 1;");
        
        addMessage("Welcome to F.R.I.D.A.Y. RPG");
        addMessage("Use WASD or arrow keys to move");
    }
    
    public void addMessage(String message) {
        Label entry = new Label("> " + message);
        entry.setFont(Font.font(GameWindow.FONT_FAMILY, 11));
        entry.setTextFill(Color.web("#aaaaaa"));
        entry.setWrapText(true);
        
        content.getChildren().add(entry);
        
        if (content.getChildren().size() > 50) {
            content.getChildren().remove(0);
        }
        
        setVvalue(1.0);
    }
}
