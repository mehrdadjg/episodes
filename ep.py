# Python >= 3.6.3
import re
import sys
import urllib.request

#
#   ██████╗ ██████╗ ███╗   ██╗███████╗████████╗ █████╗ ███╗   ██╗████████╗███████╗
#  ██╔════╝██╔═══██╗████╗  ██║██╔════╝╚══██╔══╝██╔══██╗████╗  ██║╚══██╔══╝██╔════╝
#  ██║     ██║   ██║██╔██╗ ██║███████╗   ██║   ███████║██╔██╗ ██║   ██║   ███████╗
#  ██║     ██║   ██║██║╚██╗██║╚════██║   ██║   ██╔══██║██║╚██╗██║   ██║   ╚════██║
#  ╚██████╗╚██████╔╝██║ ╚████║███████║   ██║   ██║  ██║██║ ╚████║   ██║   ███████║
#   ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝
#                                                                                 

__WS__ = r'[\s|\\n]*'

__EPISODE_INFO_PATTERN__AIR_DATE = 'airdate'
__EPISODE_INFO_PATTERN__DESCRIPTION = 'description'
__EPISODE_INFO_PATTERN__EPISODE_NAME = 'episodename'
__EPISODE_INFO_PATTERN__EPISODE_NUMBER = 'episodenumber'
__EPISODE_INFO_PATTERN__RATING = 'rating'
__EPISODE_INFO_PATTERN__SEASON_NUMBER = 'seasonnumber'
__EPISODE_INFO_PATTERN__TT = 'eptitlecode'
__EPISODE_INFO_PATTERN__VOTE_COUNT = 'votecount'
__EPISODE_INFO_PATTERN__ = (r'<div class = "list_item ([^<]*<){3}div data-const = "tt(?P<' + __EPISODE_INFO_PATTERN__TT + r'>\d+)" ([^<]*<){2}div>S(?P<' + __EPISODE_INFO_PATTERN__SEASON_NUMBER + r'>\d+), Ep(?P<' + __EPISODE_INFO_PATTERN__EPISODE_NUMBER + r'>\d+)<\/div>([^<]*<){6}div class = "airdate"> (?P<' + __EPISODE_INFO_PATTERN__AIR_DATE + r'>[^<]*)<\/div>([^<]*<){2}a\shref="/title/tt\d+/\?ref_=ttep_ep(?P=' + __EPISODE_INFO_PATTERN__EPISODE_NUMBER + r')" title = "(?P<' + __EPISODE_INFO_PATTERN__EPISODE_NAME + r'>.*)" itemprop="name" >(?P=' + __EPISODE_INFO_PATTERN__EPISODE_NAME + r')(([^<]*<){12}span class = "ipl-rating-star__rating" >(?P<' + __EPISODE_INFO_PATTERN__RATING + r'>\d+[.\d+]*)</span> <span class = "ipl-rating-star__total-votes">\((?P<' + __EPISODE_INFO_PATTERN__VOTE_COUNT + r'>\d+[,\d+]*)\)([^<]*<){294}div class = "item_description" itemprop="description"> (?P<' + __EPISODE_INFO_PATTERN__DESCRIPTION + r'>.*)<\/div> <div class = "wtw-option-standalone" data-tconst="tt(?P=' + __EPISODE_INFO_PATTERN__TT + r'))*').replace(' ', __WS__)
__EPISODE_TIME_PATTERN__DAY = 'day'
__EPISODE_TIME_PATTERN__MONTH = 'month'
__EPISODE_TIME_PATTERN__YEAR = 'year'
__EPISODE_TIME_PATTERN__ = (r'(?P<' + __EPISODE_TIME_PATTERN__DAY + r'>\d+) (?P<' + __EPISODE_TIME_PATTERN__MONTH + r'>\w+)(\.){0,1} (?P<' + __EPISODE_TIME_PATTERN__YEAR + r'>\d+)').replace(' ', __WS__)
__IMDB_EPISODES_URL__ = 'http://www.imdb.com/title/{0}/episodes'
__IMDb_FIND_URL__ = 'http://www.imdb.com/find'
__TITLE_URL_PREFIX__ = 'http://www.imdb.com/title/'
__SHOW_FIND_URL_POSTFIX__ = r'/\?ref_=fn_tt_tt_1'
__SHOW_FIND_URL_PREFIX__ = r'/title/'
__SHOW_EPISODE_COUNT_PATTERN__EC = 'episodecount'
__SHOW_EPISODE_COUNT_PATTERN__ = (r'<span class = \"bp_sub_heading\" > (?P<' + __SHOW_EPISODE_COUNT_PATTERN__EC + r'> \d+ ) episodes* < \/span >').replace(' ', __WS__)
__SHOW_NAME_YEARS_PATTERN__END_YEAR = 'eyear'
__SHOW_NAME_YEARS_PATTERN__NAME = 'name'
__SHOW_NAME_YEARS_PATTERN__START_YEAR = 'syear'
__SHOW_NAME_YEARS_PATTERN__ = (r'<meta name = \"title\" content = \"(?P<' + __SHOW_NAME_YEARS_PATTERN__NAME + r'> .+ ) \(TV M*i*n*i*-*Series (?P<' + __SHOW_NAME_YEARS_PATTERN__START_YEAR + r'> \d+ )\\xe2\\x80\\x93(?P<' + __SHOW_NAME_YEARS_PATTERN__END_YEAR + r'> [\d\s]* )\) - IMDb\" \/>').replace(' ', __WS__)
__SHOW_RATING_PATTERN__RATING = 'rating'
__SHOW_RATING_PATTERN__ = (r'<span itemprop = \"ratingValue\"> (?P<' + __SHOW_RATING_PATTERN__RATING + r'> \d+ . \d+ ) < \/span >').replace(' ', __WS__)
__SHOW_SEASON_COUNT_PATTERN__SC = 'seasoncount'
__SHOW_SEASON_COUNT_PATTERN__ = (r'< a href = \"/title/tt\d+/episodes\? season = (?P<' + __SHOW_SEASON_COUNT_PATTERN__SC + r'> \d+ )& ref_=tt_eps_sn_\d+\" > \d+ < \/a >').replace(' ', __WS__)
__SHOW_VOTE_COUNT_PATTERN__VC = 'votecount'
__SHOW_VOTE_COUNT_PATTERN__ = (r'<span .* itemprop = \"ratingCount\" > (?P<' + __SHOW_VOTE_COUNT_PATTERN__VC + r'> \d+ [,\d+ ]* ) < \/span >').replace(' ', __WS__)
__SHOW_TITLE_PATTERN__ = r'tt[\d]+'

__HEADING__ = '|%s.%s|%s|%s|%s|%s|'

__EPISODE_NO_RATING__ = '***'
__EPISODE_NO_VOTES__ = '***'

tableLen = 0

__USAGE__ = """Use: py ep.py mode [show_name show_code ...]

mode:\t\trate\t\tTo sort all the episodes by their rating
\t\tdate\t\tTo sort all the episodes by their date
\t\tvote\t\tTo sort all the episodes by their vote count

show_name:\t\t\tThe name of the show

show_code:\t\t\tThe IMDb code of the show

Examples:
ep rate "Game of Thrones":\tSorts all the Game of Thrones episodes by their ratings
ep date tt4635276:\t\tSorts all the Master of None episodes by their date

Common Mistake:
If the name of the show has multiple words, enclose it in quotation marks."""

#
#  ███████╗██╗  ██╗ ██████╗███████╗██████╗ ████████╗██╗ ██████╗ ███╗   ██╗███████╗
#  ██╔════╝╚██╗██╔╝██╔════╝██╔════╝██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║██╔════╝
#  █████╗   ╚███╔╝ ██║     █████╗  ██████╔╝   ██║   ██║██║   ██║██╔██╗ ██║███████╗
#  ██╔══╝   ██╔██╗ ██║     ██╔══╝  ██╔═══╝    ██║   ██║██║   ██║██║╚██╗██║╚════██║
#  ███████╗██╔╝ ██╗╚██████╗███████╗██║        ██║   ██║╚██████╔╝██║ ╚████║███████║
#  ╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝        ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
#                                                                                 

class NotFoundException(Exception):
    __TITLE_MSG__ = "A title with name '{0}' was not found."
    __SHOW_MSG__ = "The show's {0} was not found."
    __EPISODE_MSG__ = "The episode's {0} was not found."
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

class ConnectionException(Exception):
    __FIND_PAGE_MSG__ = "Could not connect to the IMDb find page."
    __TITLE__PAGE__MSG__ = "Could not connect to the IMDb title ({0}) page."
    __SEASON__PAGE__MSG__ = "Could not connect to the IMDb season page."
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

#
#   ██████╗██╗      █████╗ ███████╗███████╗███████╗███████╗
#  ██╔════╝██║     ██╔══██╗██╔════╝██╔════╝██╔════╝██╔════╝
#  ██║     ██║     ███████║███████╗███████╗█████╗  ███████╗
#  ██║     ██║     ██╔══██║╚════██║╚════██║██╔══╝  ╚════██║
#  ╚██████╗███████╗██║  ██║███████║███████║███████╗███████║
#   ╚═════╝╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚══════╝
#

class Show:
    def __init__(self, tt):
        self.tt = tt

    def setName(self, name):
        self.name = name

    def setStartYear(self, year):
        self.startyear = year

    def setEndYear(self, year):
        self.endyear = year

    def setRating(self, rating):
        self.rating = rating

    def setVoteCount(self, votecount):
        self.votecount = votecount

    def setEpisodeCount(self, epcount):
        self.episodecount = epcount

    def setSeasonCount(self, count):
        self.seasoncount = count

    def __str__(self):
        firstLine = ''.join([
                self.name,
                ' (' + str(self.startyear),
                ' - ',
                {True: '', False: str(self.endyear)}[self.endyear == -1] + ')'
            ])
        secondLine = ''.join([
                'Rating: ',
                str(self.rating) + '/10.0 from ' + str(self.votecount) + ' votes',
            ])
        thirdLine = ''.join([
                str(self.seasoncount) + ' season' + {True: "", False: "s"}[self.seasoncount == 1],
                " and ",
                str(self.episodecount) + ' episodes' + {True: "", False: "s"}[self.episodecount == 1],
                " listed"
            ])
        return center(firstLine, tableLen) + "\n" + center(secondLine, tableLen) + "\n" + center(thirdLine, tableLen) + "\n"

    def __repr__(self):
        return self.__str__()

class Episode:
    maxNameLen = 0
    maxSeasonLen = 0
    maxEpisodeLen = 0
    maxDateLen = 0
    maxRatingLen = 0
    maxVoteLen = 0

    def __HEADING__RATE_FILLER(self):
        return (
                    right(str(self.number[0]), max(3, Episode.maxSeasonLen + 2)),
                    left(str(self.number[1]), max(4, Episode.maxEpisodeLen + 2)),
                    {True: center(str(__EPISODE_NO_RATING__), max(8, Episode.maxRatingLen + 4)),
                     False: center(str(-self.rating), max(8, Episode.maxRatingLen + 4))}
                        [self.rating > 0],
                    center(str(self.name), max(8, Episode.maxNameLen + 4)),
                    center(self.getAirDate(), max(12, Episode.maxDateLen + 4)),
                    {True: center(str(__EPISODE_NO_VOTES__), max(9, Episode.maxVoteLen + 4)),
                     False: center(str(-self.votecount), max(9, Episode.maxVoteLen + 4))}
                        [self.votecount > 0]
                )

    def __HEADING__DATE_FILLER(self):
        return (
                    right(str(self.number[0]), max(3, Episode.maxSeasonLen + 2)),
                    left(str(self.number[1]), max(4, Episode.maxEpisodeLen + 2)),
                    center(self.getAirDate(), max(12, Episode.maxDateLen + 4)),
                    center(str(self.name), max(8, Episode.maxNameLen + 4)),
                    {True: center(str(__EPISODE_NO_RATING__), max(8, Episode.maxRatingLen + 4)),
                     False: center(str(-self.rating), max(8, Episode.maxRatingLen + 4))}
                        [self.rating > 0],
                    {True: center(str(__EPISODE_NO_VOTES__), max(9, Episode.maxVoteLen + 4)),
                     False: center(str(-self.votecount), max(9, Episode.maxVoteLen + 4))}
                        [self.votecount > 0]
                )

    def __HEADING__VOTE_FILLER(self):
        return (
                    right(str(self.number[0]), max(3, Episode.maxSeasonLen + 2)),
                    left(str(self.number[1]), max(4, Episode.maxEpisodeLen + 2)),
                    {True: center(str(__EPISODE_NO_VOTES__), max(9, Episode.maxVoteLen + 4)),
                     False: center(str(-self.votecount), max(9, Episode.maxVoteLen + 4))}
                        [self.votecount > 0],
                    center(str(self.name), max(8, Episode.maxNameLen + 4)),
                    {True: center(str(__EPISODE_NO_RATING__), max(8, Episode.maxRatingLen + 4)),
                     False: center(str(-self.rating), max(8, Episode.maxRatingLen + 4))}
                        [self.rating > 0],
                    center(self.getAirDate(), max(12, Episode.maxDateLen + 4))
                )

    def __init__(self, show):
        self.show = show

    def setName(self, name):
        self.name = name.replace('\\', '')
        if len(self.name) > Episode.maxNameLen:
            Episode.maxNameLen = len(self.name)

    def setNumber(self, season, episodeInSeason):
        self.number = (season, episodeInSeason)
        if len(str(self.number[0])) > Episode.maxSeasonLen:
            Episode.maxSeasonLen = len(str(self.number[0]))
        if len(str(self.number[1])) > Episode.maxEpisodeLen:
            Episode.maxEpisodeLen = len(str(self.number[1]))

    def getAirDate(self):
        if self.airdate[1] > 12 or self.airdate[2] > 31:
            return str(self.airdate[0])
        else:
            return str(self.airdate[2]) + ' ' + {1:  'Jan.',
                                          2:  'Feb.',
                                          3:  'Mar.',
                                          4:  'Apr.',
                                          5:  'May',
                                          6:  'June',
                                          7:  'July',
                                          8:  'Aug.',
                                          9:  'Sep.',
                                          10: 'Oct.',
                                          11: 'Nov.',
                                          12: 'Dec.'}[self.airdate[1]] + ' ' + str(self.airdate[0])

    def setAirDate(self, year, month, day):
        self.airdate = (year, month, day)
        if len(self.getAirDate()) > Episode.maxDateLen:
            Episode.maxDateLen = len(self.getAirDate())

    def setRating(self, rating):
        self.rating = rating
        if self.rating > 0:
            if len(__EPISODE_NO_RATING__) < Episode.maxRatingLen:
                Episode.maxRatingLen = len(__EPISODE_NO_RATING__)
        else:
            if len(str(-self.rating)) > Episode.maxRatingLen:
                Episode.maxRatingLen = len(str(-self.rating))

    def setVoteCount(self, votecount):
        self.votecount = votecount
        if self.votecount > 0:
            if len(__EPISODE_NO_VOTES__) < Episode.maxRatingLen:
                Episode.maxRatingLen = len(__EPISODE_NO_VOTES__)
        else:
            if len(str(-self.votecount)) > Episode.maxVoteLen:
                Episode.maxVoteLen = len(str(-self.votecount))

    def setDescription(self, description):
        self.description = description

    def __lt__(self, other):
        if sys.argv[1] == 'rate':
            return (self.rating, self.votecount) < (other.rating, other.votecount)
        elif sys.argv[1] == 'date':
            return self.airdate < other.airdate
        elif sys.argv[1] == 'vote':
            return self.votecount < other.votecount

    def __str__(self):
        if sys.argv[1] == 'rate':
            return __HEADING__ % (
                self.__HEADING__RATE_FILLER()
            )
        elif sys.argv[1] == 'date':
            return __HEADING__ % (
                self.__HEADING__DATE_FILLER()
            )
        elif sys.argv[1] == 'vote':
            return __HEADING__ % (
                self.__HEADING__VOTE_FILLER()
            )

    def __repr__(self):
        return self.__str__()

#
#  ███████╗██╗   ██╗███╗   ██╗ ██████╗████████╗██╗ ██████╗ ███╗   ██╗███████╗
#  ██╔════╝██║   ██║████╗  ██║██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║██╔════╝
#  █████╗  ██║   ██║██╔██╗ ██║██║        ██║   ██║██║   ██║██╔██╗ ██║███████╗
#  ██╔══╝  ██║   ██║██║╚██╗██║██║        ██║   ██║██║   ██║██║╚██╗██║╚════██║
#  ██║     ╚██████╔╝██║ ╚████║╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║███████║
#  ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
#                                                                            

def getTitleCode(show):
    pattern = __SHOW_TITLE_PATTERN__
    exp = re.compile(pattern)
    if exp.fullmatch(show):
        return show
    else:
        return searchForTitle(show)

def searchForTitle(show):
    try:
        url = __IMDb_FIND_URL__
        values = {'q': show,
                's': 'tt'}
        data = urllib.parse.urlencode(values)
        data = data.encode('ascii')

        req = urllib.request.Request(url, data)

        response = urllib.request.urlopen(req)
        html = response.read()
    except Exception:
        raise ConnectionException(ConnectionException.__FIND_PAGE_MSG__)

    try:
        pattern = __SHOW_FIND_URL_PREFIX__ + __SHOW_TITLE_PATTERN__ + __SHOW_FIND_URL_POSTFIX__
        m = re.search(pattern, str(html))
        return m.group(0)[len(__SHOW_FIND_URL_PREFIX__):-len(__SHOW_FIND_URL_POSTFIX__) + 1]
    except Exception:
        raise NotFoundException(NotFoundException.__TITLE_MSG__.format(show))

def getShow(tt):
    try:
        url = __TITLE_URL_PREFIX__ + tt

        response = urllib.request.urlopen(url)
        html = response.read()
    except Exception:
        raise ConnectionException(ConnectionException.__TITLE__PAGE__MSG__.format(tt))

    show = Show(tt)

    try:
        pattern = __SHOW_NAME_YEARS_PATTERN__
        m = re.search(pattern, str(html))
        show.setName(m.group(__SHOW_NAME_YEARS_PATTERN__NAME))
        show.setStartYear(int(m.group(__SHOW_NAME_YEARS_PATTERN__START_YEAR)))
        eyear = m.group(__SHOW_NAME_YEARS_PATTERN__END_YEAR)
        if eyear == ' ':
            show.setEndYear(-1)
        else:
            show.setEndYear(int(m.group(__SHOW_NAME_YEARS_PATTERN__END_YEAR)))
    except Exception:
        raise NotFoundException(NotFoundException.__SHOW_MSG__.format('name and/or years'))

    try:
        pattern = __SHOW_RATING_PATTERN__
        m = re.search(pattern, str(html))
        show.setRating(float(m.group(__SHOW_RATING_PATTERN__RATING)))
    except Exception:
        raise NotFoundException(NotFoundException.__SHOW_MSG__.format('rating'))

    try:
        pattern = __SHOW_VOTE_COUNT_PATTERN__
        m = re.search(pattern, str(html))
        show.setVoteCount(int(m.group(__SHOW_VOTE_COUNT_PATTERN__VC).replace(',','')))
    except Exception:
        raise NotFoundException(NotFoundException.__SHOW_MSG__.format('vote count'))

    try:
        pattern = __SHOW_EPISODE_COUNT_PATTERN__
        m = re.search(pattern, str(html))
        show.setEpisodeCount(int(m.group(__SHOW_EPISODE_COUNT_PATTERN__EC)))
    except Exception:
        raise NotFoundException(NotFoundException.__SHOW_MSG__.format('episode count'))

    try:
        pattern = __SHOW_SEASON_COUNT_PATTERN__
        m = re.search(pattern, str(html))
        show.setSeasonCount(int(m.group(__SHOW_SEASON_COUNT_PATTERN__SC)))
    except Exception:
        raise NotFoundException(NotFoundException.__SHOW_MSG__.format('season count'))

    return show

def monthOf(monthStr):
    if 'january'.startswith(monthStr.lower()):
        return 1
    elif 'february'.startswith(monthStr.lower()):
        return 2
    elif 'march'.startswith(monthStr.lower()):
        return 3
    elif 'april'.startswith(monthStr.lower()):
        return 4
    elif 'may'.startswith(monthStr.lower()):
        return 5
    elif 'june'.startswith(monthStr.lower()):
        return 6
    elif 'july'.startswith(monthStr.lower()):
        return 7
    elif 'august'.startswith(monthStr.lower()):
        return 8
    elif 'september'.startswith(monthStr.lower()):
        return 9
    elif 'october'.startswith(monthStr.lower()):
        return 10
    elif 'november'.startswith(monthStr.lower()):
        return 11
    elif 'december'.startswith(monthStr.lower()):
        return 12
    else:
        return 13

def center(text, maxLength):
    dif = maxLength - len(text)
    if dif % 2 == 0:
        return ' '*(dif//2) + text + ' '*(dif//2)
    else:
        return ' '*((dif+1)//2) + text + ' '*((dif-1)//2)

def right(text, maxLength):
    return ' '*(maxLength - len(text)) + text

def left(text, maxLength):
    return text + ' '*(maxLength - len(text))

def printResult(show, episodes):
    global tableLen
    if sys.argv[1] == 'rate':
        heading = __HEADING__ % (
            right('S', max(3, Episode.maxSeasonLen + 2)),
            left('EP', max(4, Episode.maxEpisodeLen + 2)),
            center('RATE', max(8, Episode.maxRatingLen + 4)),
            center('NAME', max(8, Episode.maxNameLen + 4)),
            center('AIR DATE', max(12, Episode.maxDateLen + 4)),
            center('VOTES', max(9, Episode.maxVoteLen + 4))
        )
    elif sys.argv[1] == 'date':
        heading = __HEADING__ % (
            right('S', max(3, Episode.maxSeasonLen + 2)),
            left('EP', max(4, Episode.maxEpisodeLen + 2)),
            center('AIR DATE', max(12, Episode.maxDateLen + 4)),
            center('NAME', max(8, Episode.maxNameLen + 4)),
            center('RATE', max(8, Episode.maxRatingLen + 4)),
            center('VOTES', max(9, Episode.maxVoteLen + 4))
        )
    elif sys.argv[1] == 'vote':
        heading = __HEADING__ % (
            right('S', max(3, Episode.maxSeasonLen + 2)),
            left('EP', max(4, Episode.maxEpisodeLen + 2)),
            center('VOTES', max(9, Episode.maxVoteLen + 4)),
            center('NAME', max(8, Episode.maxNameLen + 4)),
            center('RATE', max(8, Episode.maxRatingLen + 4)),
            center('AIR DATE', max(12, Episode.maxDateLen + 4)),
        )
    tableLen = len(heading)
    heading += "\n" + '-'*tableLen

    leftLen = tableLen // 3
    rightLen = tableLen // 3 + (tableLen % 3)
    centerLen = tableLen // 3

    print('*'*tableLen)
    print('*'*leftLen + center(str(i), centerLen) + '*'*rightLen)
    print('*'*tableLen)

    print(show)

    print(heading)
                
    for ep in sorted(episodes):
        print(ep)

    print('='*tableLen)

def getEpisodes(show):
    episodes = []
    for i in range(1, show.seasoncount + 1):
        try:
            url = __IMDB_EPISODES_URL__.format(show.tt)
            values = {'season': str(i)}
            data = urllib.parse.urlencode(values)
            data = data.encode('ascii')

            req = urllib.request.Request(url, data)

            response = urllib.request.urlopen(req)
            html = response.read()
        except Exception:
            raise ConnectionException(ConnectionException.__SEASON__PAGE__MSG__)

        try:
            pattern = __EPISODE_INFO_PATTERN__
            for groups in re.finditer(pattern, str(html)):
                ep = Episode(show)

                ep.setName(groups[__EPISODE_INFO_PATTERN__EPISODE_NAME])
                ep.setNumber(groups[__EPISODE_INFO_PATTERN__SEASON_NUMBER], groups[__EPISODE_INFO_PATTERN__EPISODE_NUMBER])
                try:
                    year = int(groups[__EPISODE_INFO_PATTERN__AIR_DATE].strip('\\n '))
                    ep.setAirDate(year, 13, 33)
                except ValueError:
                    date_pattern = __EPISODE_TIME_PATTERN__
                    m = re.search(date_pattern, groups[__EPISODE_INFO_PATTERN__AIR_DATE].strip('\\n '))
                    ep.setAirDate(int(m.group(__EPISODE_TIME_PATTERN__YEAR)), monthOf(m.group(__EPISODE_TIME_PATTERN__MONTH)), int(m.group(__EPISODE_TIME_PATTERN__DAY)))

                if groups[__EPISODE_INFO_PATTERN__RATING] == None:
                    ep.setRating(1.0)
                else:
                    ep.setRating(-float(groups[__EPISODE_INFO_PATTERN__RATING]))

                if groups[__EPISODE_INFO_PATTERN__VOTE_COUNT] == None:
                    ep.setVoteCount(1)
                else:
                    ep.setVoteCount(-1 * int(groups[__EPISODE_INFO_PATTERN__VOTE_COUNT].replace(',', '')))

                ep.setDescription(groups[__EPISODE_INFO_PATTERN__DESCRIPTION])

                episodes.append(ep)
        except Exception as e:
            print(e)
            raise NotFoundException(NotFoundException.__EPISODE_MSG__.format('information'))

    return episodes        

#
#  ███╗   ███╗ █████╗ ██╗███╗   ██╗
#  ████╗ ████║██╔══██╗██║████╗  ██║
#  ██╔████╔██║███████║██║██╔██╗ ██║
#  ██║╚██╔╝██║██╔══██║██║██║╚██╗██║
#  ██║ ╚═╝ ██║██║  ██║██║██║ ╚████║
#  ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝
#                                  

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__USAGE__)
    else:
        if sys.argv[1] not in ['rate', 'date', 'vote']:
            print(__USAGE__)
        else:
            i = 0
            for show in sys.argv[2:]:
                i = i + 1
                show = show.lower()
                try:
                    tt = getTitleCode(show)
                except ConnectionException as e:
                    print(e)
                    break
                except NotFoundException as e:
                    print(e)
                    continue

                try:
                    show = getShow(tt)
                except ConnectionException as e:
                    print(e)
                    break
                except NotFoundException as e:
                    print(e)
                    continue

                try:
                    episodes = getEpisodes(show)
                except ConnectionException as e:
                    print(e)
                    break
                except NotFoundException as e:
                    print(e)
                    break

                printResult(show, episodes)
