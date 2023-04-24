# Diseño software


## Diagrama estático
### Diagrama de clases
```mermaid
classDiagram
    Controller <--> View
    Controller <--> Model
    Controller: __init__(self, model, view)
    Controller: main(self)
    Controller: searchClicked(self, button, *args)
    Controller: homeClicked(self, button, *args)
    Controller: search_command(self, command_searched)
    class View{
      struct __gsignals__
      __init__(self, **kw)
      run(self)
      quit(cls, widget)
      show_home(self)
      hide_home(self)
      display_command(self, result)
      show_search(self)
      hide_search(self)
      connect_search_clicked(self, fun)
      connect_home_clicked(self, fun)
}
    class Model{
      search_command(self, command)
      parse_text(self, text: str)
      parse_chunk(self, chunk: str)
      get_cheatsheet(self, command: str)
    
}
```
## Diagramas dinámicos
### Diagrama de clases
```mermaid
sequenceDiagram
    View->>+Controller: searchClicked()
    Controller->>+Controller: search_command()
    Controller->>+Model: search_command()
    Model-->>-Controller: 
    Controller-->>-View: 
```      
