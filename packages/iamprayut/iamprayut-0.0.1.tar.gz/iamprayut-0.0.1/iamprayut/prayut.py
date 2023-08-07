class Prayut:
    """
    คลาสPrayutคือข้อมูลที่เกี่ยวข้องกับประยุทธ์ จันโอชา
    """
    def __init__(self):
        self.name = 'Prayut Chan-o-cha'
        self.page = 'https://www.facebook.com/prayutofficial/'

    def show_name(self):
        print(f'Hello my name is {self.name}')
    
    def show_page(self):
        print(self.page)

    def about(self):
        text = """
        Prayut Chan-o-cha (sometimes spelled Prayuth Chan-ocha; Thai: ประยุทธ์ จันทร์โอชา,(born 21 March 1954) is a Thai politician and retired army officer who has served as the Prime Minister of Thailand since he seized power in a military coup in 2014. He is concurrently the Minister of Defence, a position he has held in his own government since 2019. Prayut served as Commander in Chief of Royal Thai Army from 2010 to 2014 and led the 2014 Thai coup d'état which installed the National Council for Peace and Order (NCPO), the military junta which governed Thailand between 22 May 2014 and 10 July 2019."""
        print(text)
    def show_art(self):
        text = """
        /                       \\
        /X/                       \X\\
        |XX\         _____         /XX|
        |XXX\     _/       \_     /XXX|___________
        \XXXXXXX             XXXXXXX/            \\\\
        \XXXX    /     \    XXXXX/                \\\\
                |   0     0   |                         \\
                |           |                           \\
                \         /                            |______//
                \       /                             |
                    | O_O | \                            |
                    \ _ /   \________________           |
                                | |  | |      \         /
        No Bullshit,          / |  / |       \______/
        Please...            \ |  \ |        \ |  \ |
                            __| |__| |      __| |__| |
                            |___||___|      |___||___|
        """
        print(text)

    


if __name__ == '__main__':
    mayor = Prayut()
    mayor.show_name()
    mayor.show_page()
    mayor.about()
    mayor.show_art()