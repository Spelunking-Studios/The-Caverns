#include <iostream>
#include <window.hpp>
#include <sprite.hpp>

class Engine {
    public:
        // Constructor & Destructor
        Engine();
        // Properties
        Window* window;
        void (*eventHandler)(Engine *e, sf::Event event);
        void (*mainLoopFn)(Engine *e, sf::RenderWindow *window);
        sf::Color clearColor = sf::Color::Black;
        // Methods
        void run(void);
        void stop(void);
        void setMainLoop(void (*fn)(Engine *e, sf::RenderWindow *window));
        void setEventHandler(void (*callback)(Engine *e, sf::Event event));
        void processEvents(void);
        void clearScreen(void);
        void setClearColor(sf::Color c);
};

inline Engine::Engine() {
    window = new Window();
}

inline void Engine::run(void) {
    std::cout << "Running engine..." << std::endl;
    while (window->sfmlWindow->isOpen()) {
        (*mainLoopFn)(this, window->sfmlWindow);
    }
}

inline void Engine::stop(void) {
    window->sfmlWindow->close();
}

inline void Engine::setMainLoop(void (*fn)(Engine *e, sf::RenderWindow *window)) {
    mainLoopFn = fn;
}

inline void Engine::setEventHandler(void (*callback)(Engine *e, sf::Event event)) {
    eventHandler = callback;
}

inline void Engine::processEvents(void) {
    sf::Event event;
    while (window->sfmlWindow->pollEvent(event)) {
        (*eventHandler)(this, event);
    }
}

inline void Engine::clearScreen(void) {
    window->sfmlWindow->clear(clearColor);
}

inline void Engine::setClearColor(sf::Color c) {
    clearColor = c;
}