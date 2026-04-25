package com.friday.rpg.ui;

import com.friday.rpg.combat.Battle;
import com.friday.rpg.core.GameState;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.ProgressBar;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;

public class BattleView extends BorderPane {
    
    private GameState gameState;
    private VBox actionMenu;
    private VBox combatLog;
    private HBox enemyPanel;
    private HBox playerPanel;
    
    public BattleView(GameState gameState) {
        this.gameState = gameState;
        setStyle("-fx-background-color: #0a0a0a;");
        
        enemyPanel = new HBox(20);
        enemyPanel.setAlignment(Pos.CENTER);
        enemyPanel.setPadding(new Insets(20));
        setTop(enemyPanel);
        
        BorderPane bottomPanel = new BorderPane();
        bottomPanel.setStyle("-fx-background-color: #0a0a0a; -fx-border-color: #00ff41; -fx-border-width: 2 0 0 0;");
        bottomPanel.setPrefHeight(200);
        
        actionMenu = createActionMenu();
        bottomPanel.setLeft(actionMenu);
        
        combatLog = new VBox(2);
        combatLog.setPadding(new Insets(10));
        bottomPanel.setCenter(combatLog);
        
        playerPanel = new HBox(20);
        playerPanel.setAlignment(Pos.CENTER);
        playerPanel.setPadding(new Insets(10));
        playerPanel.setPrefWidth(250);
        bottomPanel.setRight(playerPanel);
        
        setBottom(bottomPanel);
    }
    
    public void setGameState(GameState gameState) {
        this.gameState = gameState;
        update();
    }
    
    private VBox createActionMenu() {
        VBox menu = new VBox(5);
        menu.setPadding(new Insets(10));
        menu.setPrefWidth(150);
        menu.setStyle("-fx-border-color: #00ff41; -fx-border-width: 0 1 0 0;");
        
        menu.getChildren().addAll(
            createActionButton("Attack", () -> executeAction("attack")),
            createActionButton("Defend", () -> executeAction("defend")),
            createActionButton("Flee", () -> executeAction("flee"))
        );
        
        return menu;
    }
    
    private Button createActionButton(String text, Runnable action) {
        Button btn = new Button(text);
        btn.setFont(Font.font(GameWindow.FONT_FAMILY, 12));
        btn.setStyle("-fx-background-color: transparent; -fx-text-fill: #00ff41; -fx-border-color: #00ff41; -fx-padding: 8 12; -fx-min-width: 120;");
        btn.setOnAction(e -> action.run());
        return btn;
    }
    
    private void executeAction(String action) {
        Battle battle = gameState.getCurrentBattle();
        if (battle == null || !battle.isPlayerTurn()) return;
        
        switch (action) {
            case "attack": battle.playerAttack(); break;
            case "defend": battle.playerDefend(); break;
            case "flee": 
                if (battle.playerFlee()) gameState.endBattle(false);
                break;
        }
        
        update();
        
        if (battle.getState() == Battle.BattleState.ENEMY_TURN) {
            new Thread(() -> {
                try {
                    Thread.sleep(1000);
                    javafx.application.Platform.runLater(() -> {
                        battle.executeEnemyTurn();
                        update();
                        if (battle.getState() == Battle.BattleState.VICTORY) {
                            gameState.endBattle(true);
                        }
                    });
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }).start();
        }
    }
    
    public void update() {
        Battle battle = gameState.getCurrentBattle();
        if (battle == null) return;
        
        enemyPanel.getChildren().clear();
        VBox enemyBox = new VBox(5);
        enemyBox.setAlignment(Pos.CENTER);
        
        Label enemyName = new Label(battle.getEnemy().getName());
        enemyName.setFont(Font.font(GameWindow.FONT_FAMILY, FontWeight.BOLD, 14));
        enemyName.setTextFill(Color.web("#ff4444"));
        
        ProgressBar enemyHP = new ProgressBar(battle.getEnemy().getHealthPercent());
        enemyHP.setPrefWidth(150);
        enemyHP.setStyle("-fx-accent: #ff4444;");
        
        enemyBox.getChildren().addAll(enemyName, enemyHP);
        enemyPanel.getChildren().add(enemyBox);
        
        playerPanel.getChildren().clear();
        VBox playerBox = new VBox(5);
        playerBox.setAlignment(Pos.CENTER);
        
        Label playerName = new Label(gameState.getPlayer().getName());
        playerName.setFont(Font.font(GameWindow.FONT_FAMILY, FontWeight.BOLD, 14));
        playerName.setTextFill(Color.web("#00ff41"));
        
        ProgressBar playerHP = new ProgressBar(gameState.getPlayer().getHealthPercent());
        playerHP.setPrefWidth(150);
        playerHP.setStyle("-fx-accent: #00ff41;");
        
        playerBox.getChildren().addAll(playerName, playerHP);
        playerPanel.getChildren().add(playerBox);
        
        combatLog.getChildren().clear();
        for (String msg : battle.getCombatLog()) {
            Label entry = new Label("> " + msg);
            entry.setFont(Font.font(GameWindow.FONT_FAMILY, 11));
            entry.setTextFill(Color.web("#aaaaaa"));
            combatLog.getChildren().add(entry);
        }
    }
}
