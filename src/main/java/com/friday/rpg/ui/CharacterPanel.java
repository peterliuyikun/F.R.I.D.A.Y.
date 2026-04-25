package com.friday.rpg.ui;

import com.friday.rpg.core.GameState;
import com.friday.rpg.core.Player;
import javafx.geometry.Insets;
import javafx.scene.control.Label;
import javafx.scene.control.ProgressBar;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;

public class CharacterPanel extends VBox {
    
    private GameState gameState;
    private Label nameLabel;
    private ProgressBar hpBar, mpBar, xpBar;
    private Label strLabel, dexLabel, intLabel, lvlLabel;
    
    public CharacterPanel(GameState gameState) {
        this.gameState = gameState;
        setSpacing(5);
        setPadding(new Insets(10));
        
        Label title = new Label("CHARACTER");
        title.setFont(Font.font(GameWindow.FONT_FAMILY, FontWeight.BOLD, 14));
        title.setTextFill(Color.web("#00ff41"));
        
        nameLabel = new Label("Unknown");
        nameLabel.setFont(Font.font(GameWindow.FONT_FAMILY, 12));
        nameLabel.setTextFill(Color.web("#ffffff"));
        
        hpBar = createBar("#00ff41");
        mpBar = createBar("#4444ff");
        xpBar = createBar("#ffaa00");
        
        GridPane statsGrid = new GridPane();
        statsGrid.setHgap(20);
        statsGrid.setVgap(5);
        statsGrid.setPadding(new Insets(10, 0, 0, 0));
        
        strLabel = createStatLabel("10");
        dexLabel = createStatLabel("10");
        intLabel = createStatLabel("10");
        lvlLabel = createStatLabel("1");
        
        statsGrid.add(createStatNameLabel("STR"), 0, 0);
        statsGrid.add(strLabel, 1, 0);
        statsGrid.add(createStatNameLabel("DEX"), 0, 1);
        statsGrid.add(dexLabel, 1, 1);
        statsGrid.add(createStatNameLabel("INT"), 0, 2);
        statsGrid.add(intLabel, 1, 2);
        statsGrid.add(createStatNameLabel("LVL"), 0, 3);
        statsGrid.add(lvlLabel, 1, 3);
        
        getChildren().addAll(title, nameLabel, hpBar, mpBar, xpBar, statsGrid);
    }
    
    private ProgressBar createBar(String color) {
        ProgressBar bar = new ProgressBar(1.0);
        bar.setPrefWidth(250);
        bar.setStyle("-fx-accent: " + color + ";");
        return bar;
    }
    
    private Label createStatNameLabel(String text) {
        Label label = new Label(text);
        label.setFont(Font.font(GameWindow.FONT_FAMILY, 10));
        label.setTextFill(Color.web("#888888"));
        return label;
    }
    
    private Label createStatLabel(String text) {
        Label label = new Label(text);
        label.setFont(Font.font(GameWindow.FONT_FAMILY, FontWeight.BOLD, 10));
        label.setTextFill(Color.web("#00ff41"));
        return label;
    }
    
    public void setGameState(GameState gameState) {
        this.gameState = gameState;
        update();
    }
    
    public void update() {
        if (gameState == null || gameState.getPlayer() == null) return;
        
        Player p = gameState.getPlayer();
        nameLabel.setText(p.getName());
        hpBar.setProgress(p.getHealthPercent());
        mpBar.setProgress(p.getManaPercent());
        xpBar.setProgress(p.getExperiencePercent());
        strLabel.setText(String.valueOf(p.getStrength()));
        dexLabel.setText(String.valueOf(p.getDexterity()));
        intLabel.setText(String.valueOf(p.getIntelligence()));
        lvlLabel.setText(String.valueOf(p.getLevel()));
    }
}
