import json
from data.course import Course
from data.group import Group


class Parser(object):

    def parse(self, data):
        opleiding = Group(data['opleiding']['naam'], 'Opleiding', data['opleiding']['min_studiepunten'],
                             data['opleiding']['max_studiepunten'], data['opleiding']['fases'])
        avo = Group('Algemeen_Vormend', 'AVO', data['opleiding']['avo']['min_studiepunten'],
                       data['opleiding']['avo']['max_studiepunten'], opleiding.stages)
        verdere_specialisatie = Group('Verdere', 'Verdere_Specialisatie',
                                         data['opleiding']['verdere_specialisatie']['min_studiepunten'],
                                         data['opleiding']['verdere_specialisatie']['max_studiepunten'],
                                         opleiding.stages)

        specialisaties = list()
        bachelor_verbredend = list()

        for c in data['opleiding']['vakken']['verplicht']:
            course = Course(c['code'], c['naam'], c['punten'], c['fases'], c['semester'], None, False)
            opleiding.add_mandatory_course(course)
        for c in data['opleiding']['vakken']['keuze']:
            course = Course(c['code'], c['naam'], c['punten'], c['fases'], c['semester'], None, False)
            opleiding.add_optional_course(course)

        for c in data['opleiding']['avo']['vakken']['verplicht']:
            course = Course(c['code'], c['naam'], c['punten'], c['fases'], c['semester'], None, False)
            avo.add_mandatory_course(course)
        for c in data['opleiding']['avo']['vakken']['keuze']:
            course = Course(c['code'], c['naam'], c['punten'], c['fases'], c['semester'], None, False)
            avo.add_optional_course(course)

        for c in data['opleiding']['verdere_specialisatie']['vakken']['verplicht']:
            course = Course(c['code'], c['naam'], c['punten'], c['fases'], c['semester'], None, False)
            verdere_specialisatie.add_mandatory_course(course)
        for c in data['opleiding']['verdere_specialisatie']['vakken']['keuze']:
            course = Course(c['code'], c['naam'], c['punten'], c['fases'], c['semester'], None, False)
            verdere_specialisatie.add_optional_course(course)

        for bv in data['opleiding']['bachelor_verbredend']:
            verbredend = Group(bv['naam'], 'Bachelor_Verbredend', 0, 0, opleiding.stages)
            for c in bv['vakken']['verplicht']:
                course = Course(c['code'], c['naam'], c['punten'], c['fases'], c['semester'], None, False)
                verbredend.add_mandatory_course(course)
            for c in bv['vakken']['keuze']:
                course = Course(c['code'], c['naam'], c['punten'], c['fases'], c['semester'], None, False)
                verbredend.add_optional_course(course)
            bachelor_verbredend.append(verbredend)
            opleiding.add_group(verbredend)

        for spe in data['opleiding']['specialisaties']:
            specialisatie = Group(spe['naam'], 'Specialisatie', 0, 0, opleiding.stages)
            for c in spe['vakken']['verplicht']:
                course = Course(c['code'], c['naam'], c['punten'], c['fases'], c['semester'], None, False)
                specialisatie.add_mandatory_course(course)
            for c in spe['vakken']['keuze']:
                course = Course(c['code'], c['naam'], c['punten'], c['fases'], c['semester'], None, False)
                specialisatie.add_optional_course(course)
            specialisaties.append(specialisatie)
            opleiding.add_group(specialisatie)

        opleiding.add_group(verdere_specialisatie)
        opleiding.add_group(avo)

        return opleiding

    def print_domain(self, opleiding):
        # domeinen
        strFase = 'Fase = {1..' + str(opleiding.stages) + '}'
        strVak = 'Vak = {'
        strVakgroep = 'VakGroep = {'
        strStudiepunten = 'Studiepunten = {0..' + str(opleiding.max) + '}'

        # predicaten
        strIsType = 'IsType = {'
        strVerplicht = 'Verplicht = {'
        strInFase = 'InFase = {'
        strInVakgroep = 'InVakGroep = {'
        strGeselecteerd = 'Geselecteerd<ct> = {'
        strGeenInteresse = 'GeenInteresse = {'

        # functies
        strInSemester = 'InSemester<ct> = {'
        strMinAantalStudiepunten = 'MinAantalStudiepunten<ct> = {'
        strMaxAantalStudiepunten = 'MaxAantalStudiepunten<ct> = {'
        strAantalStudiepunten = 'AantalStudiepunten<ct> = {'

        strVak += opleiding.print_course() + '}'
        strIsType += opleiding.print_is_type() + '}'
        strVerplicht += opleiding.print_mandatory_courses() + '}'
        strInFase += opleiding.print_in_stage() + '}'
        strInVakgroep += opleiding.print_in_group() + '}'
        strGeselecteerd += opleiding.print_selected() + '}'
        strGeenInteresse += opleiding.print_not_interested() + '}'
        strInSemester += opleiding.print_in_term() + '}'
        strMinAantalStudiepunten += opleiding.print_min_ects() + '}'
        strMaxAantalStudiepunten += opleiding.print_max_ects() + '}'
        strAantalStudiepunten += opleiding.print_amount_of_ects() + '}'
        strVakgroep += opleiding.print_group() + '}'

        s = ''
        s += strFase + '\n'
        s += strVak + '\n'
        s += strVakgroep + '\n'
        s += strStudiepunten + '\n'
        s += strIsType + '\n'
        s += strVerplicht + '\n'
        s += strInFase + '\n'
        s += strInVakgroep + '\n'
        s += strInSemester + '\n'
        s += strMinAantalStudiepunten + '\n'
        s += strMaxAantalStudiepunten + '\n'
        s += strAantalStudiepunten + '\n'
        s += strGeselecteerd + '\n'
        s += strGeenInteresse + '\n'

        return s

    def print_explanation(self, opleiding):
        # domeinen
        strFase = 'Fase = {1..' + str(opleiding.stages) + '}'
        strVak = 'Vak = {'
        strVakgroep = 'VakGroep = {'
        strStudiepunten = 'Studiepunten = {0..' + str(opleiding.max) + '}'

        # predicaten
        strIsType = 'IsType = {'
        strVerplicht = 'Verplicht = {'
        strInFase = 'InFase = {'
        strInVakgroep = 'InVakGroep = {'
        strGeselecteerd = 'Geselecteerd<ct> = {'
        strNietGeselecteerd = 'NietGeselecteerd = {'

        # functies
        strMinAantalStudiepunten = 'MinAantalStudiepunten<ct> = {'
        strMaxAantalStudiepunten = 'MaxAantalStudiepunten<ct> = {'
        strAantalStudiepunten = 'AantalStudiepunten<ct> = {'

        strVak += opleiding.print_course() + '}'
        strIsType += opleiding.print_is_type() + '}'
        strVerplicht += opleiding.print_mandatory_courses() + '}'
        strInFase += opleiding.print_in_stage() + '}'
        strInVakgroep += opleiding.print_in_group() + '}'
        strGeselecteerd += opleiding.print_selected() + '}'
        strNietGeselecteerd += opleiding.print_not_interested() + '}'
        strMinAantalStudiepunten += opleiding.print_min_ects() + '}'
        strMaxAantalStudiepunten += opleiding.print_max_ects() + '}'
        strAantalStudiepunten += opleiding.print_amount_of_ects() + '}'
        strVakgroep += opleiding.print_group() + '}'

        s = ''
        s += strFase + '\n'
        s += strVak + '\n'
        s += strVakgroep + '\n'
        s += strStudiepunten + '\n'
        s += strIsType + '\n'
        s += strVerplicht + '\n'
        s += strInFase + '\n'
        s += strInVakgroep + '\n'
        s += strMinAantalStudiepunten + '\n'
        s += strMaxAantalStudiepunten + '\n'
        s += strAantalStudiepunten + '\n'
        s += strGeselecteerd + '\n'
        s += strNietGeselecteerd + '\n'

        return s

    def read(self, file):
        with open(file) as data:
            domain = json.load(data)
        return self.parse(domain)
