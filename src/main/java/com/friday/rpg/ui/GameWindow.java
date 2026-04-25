package com.friday.rpg.ui;

import com.friday.rpg.core.GameState;
import javafx.application.Platform;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;
import javafx.stage.Stage;

public class GameWindow {
    
    private Stage stage;
    private GameState gameState;
    private Scene mainScene;
    
    private MapView mapView;
    private BattleView battleView;
    private CharacterPanel charPanel;
    private InventoryPanel invPanel;
    private CombatLog combatLog;
    
    public static final Color TERMINAL_GREEN = Color.web("#00ff41");
    public static final String FONT_FAMILY = "Courier New";
    
    public void initialize(Stage primaryStage) {
        this.stage = primaryStage;
        this.gameState = new GameState();
        
        BorderPane root = createMainLayout();
        mainScene = new Scene(root, 1200, 800);
        mainScene.setFill(Color.web("#0a0a0a"));
        
        primaryStage.setTitle("F.R.I.D.A.Y. - KOTOR RPG");
        primaryStage.setScene(mainScene);
        primaryStage.setMinWidth(1000);
        primaryStage.setMinHeight(700);
        primaryStage.show();
        
        showCharacterCreation();
    }
    
    private BorderPane createMainLayout() {
        BorderPane root = new BorderPane();
        root.setStyle("-fx-background-color: #0a0a0a;");
        
        StackPane centerPane = new StackPane();
        mapView = new MapView(gameState);
        battleView = new BattleView(gameState);
        centerPane.getChildren().addAll(mapView, battleView);
        battleView.setVisible(false);
        root.setCenter(centerPane);
        
        VBox rightPanel = new VBox(10);
        rightPanel.setPadding(new Insets(10));
        rightPanel.setStyle("-fx-background-color: #0a0a0a; -fx-border-color: #00ff41; -fx-border-width: 0 0 0 2;");
        rightPanel.setPrefWidth(300);
        
        charPanel = new CharacterPanel(gameState);
        invPanel = new InventoryPanel(gameState);
        
        rightPanel.getChildren().addAll(charPanel, new Separator(), invPanel);
        VBox.setVgrow(invPanel, Priority.ALWAYS);
        root.setRight(rightPanel);
        
        VBox bottomPanel = new VBox(5);
        bottomPanel.setPadding(new Insets(10));
        bottomPanel.setStyle("-fx-background-color: #0a0a0a; -fx-border-color: #00ff41; -fx-border-width: 2 0 0 0;");
        bottomPanel.setPrefHeight(200);
        
        combatLog = new CombatLog();
        HBox controls = createControls();
        
        bottomPanel.getChildren().addAll(combatLog, controls);
        VBox.setVgrow(combatLog, Priority.ALWAYS);
        root.setBottom(bottomPanel);
        
        return root;
    }
    
    private HBox createControls() {
        HBox controls = new HBox(10);
        controls.setPadding(new Insets(5));
        
        Button btnAdventure = createButton("ADVENTURE", true);
        Button btnPVP = createButton("PVP ARENA", false);
        
        btnAdventure.setOnAction(e -> setMode(GameState.State.EXPLORING));
        btnPVP.setOnAction(e -> setMode(GameState.State.PVP_LOBBY));
        
        controls.getChildren().addAll(btnAdventure, btnPVP);
        return controls;
    }
    
    private Button createButton(String text, boolean active) {
        Button btn = new Button(text);
        btn.setFont(Font.font(FONT_FAMILY, FontWeight.BOLD, 12));
        
        String activeStyle = "-fx-background-color: #00ff41; -fx-text-fill: #0a0a0a; -fx-border-color: #00ff41; -fx-padding: 8 15;";
        String inactiveStyle = "-fx-background-color: transparent; -fx-text-fill: #00ff41; -fx-border-color: #00ff41; -fx-padding: 8 15;";
        
        btn.setStyle(active ? activeStyle : inactiveStyle);
        return btn;
    }
    
    private void showCharacterCreation() {
        TextInputDialog dialog = new TextInputDialog("Player");
        dialog.setTitle("Character Creation");
        dialog.setHeaderText("Enter your character name");
        dialog.setContentText("Name:");
        
        dialog.showAndWait().ifPresent(name -> {
            if (!name.trim().isEmpty()) {
                startNewGame(name.trim());
            }
        });
    }
    
    private void startNewGame(String playerName) {
        gameState.initializeNewGame(playerName);
        gameState.addListener(state -> Platform.runLater(this::updateUI));
        
        mapView.setGameState(gameState);
        battleView.setGameState(gameState);
        charPanel.setGameState(gameState);
        invPanel.setGameState(gameState);
        
        updateUI();
    }
    
    private void setMode(GameState.State state) {
        gameState.setCurrentState(state);
        if (state == GameState.State.BATTLE) {
            mapView.setVisible(false);
            battleView.setVisible(true);
        } else {
            mapView.setVisible(true);
            battleView.setVisible(false);
        }
    }
    
    private void updateUI() {
        charPanel.update();
        invPanel.update();
        mapView.render();
        if (gameState.getCurrentState() == GameState.State.BATTLE) {
            battleView.update();
        }
    }
}
