import tonex_actions as ta
import tonex_gui as tg

if __name__ == "__main__":
    tonexActions = ta.TonexActions()
    tonexApp = tg.TonexApp(tonexActions)
    tonexApp.mainloop()
