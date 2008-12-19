""" Python library for interacting with Project Vote Smart API.

    Project Vote Smart's API (http://www.votesmart.org/services_api.php)
    provides rich biographical data, including data on votes, committee
    assignments, and much more.
"""

__author__ = "James Turk (jturk@sunlightfoundation.com)"
__version__ = "0.2.0"
__copyright__ = "Copyright (c) 2008 Sunlight Labs"
__license__ = "BSD"

import urllib, urllib2
try:
    import json
except ImportError:
    import simplejson as json

class VotesmartApiError(Exception):
    """ Exception for Sunlight API errors """
    
class VotesmartApiObject(object):
    def __init__(self, d):
        self.__dict__ = d
        
class Address(object):
    def __init__(self, d):
        self.__dict__.update(d['address'])
        self.__dict__.update(d['phone'])
        self.__dict__.update(d['notes'])
    
class WebAddress(VotesmartApiObject):
    def __str__(self):
        return self.webAddress
    
class Bio(object):
    def __init__(self, d):
        #self.__dict__.update(d['election'])
        #self.__dict__.update(d['office'])
        self.__dict__.update(d['candidate'])
    
class AddlBio(VotesmartApiObject):
    def __str__(self):
        return ': '.join((self.name, self.data))
    
class Candidate(VotesmartApiObject):
    def __str__(self):
        return ' '.join((self.firstName, self.lastName))
        
class CommitteeType(VotesmartApiObject):
    def __str__(self):
        return self.name

class Committee(VotesmartApiObject):
    def __str__(self):
        return self.name
    
class CommitteeDetail(VotesmartApiObject):
    def __str__(self):
        return self.name

class CommitteeMember(VotesmartApiObject):
    def __str__(self):
        return ' '.join((self.title, self.firstName, self.lastName))

class District(VotesmartApiObject):
    def __str__(self):
        return self.name
    
class Election(VotesmartApiObject):
    def __init__(self, d):
        stages = [ElectionStage(s) for s in d.pop('stage')]
        self.__dict__ = d
        self.stages = stages
    
    def __str__(self):
        return self.name
    
class ElectionStage(VotesmartApiObject):
    def __str__(self):
        return '%s (%s)' % (self.name, self.electionDate)    

class Official(VotesmartApiObject):
    def __str__(self):
        return ' '.join((self.title, self.firstName, self.lastName))
    
class LeadershipPosition(VotesmartApiObject):
    def __str__(self):
        return self.name
    
class Locality(VotesmartApiObject):
    def __str__(self):
        return self.name
    
class Measure(VotesmartApiObject):
    def __str__(self):
        return self.title
    
class MeasureDetail(VotesmartApiObject):
    def __str__(self):
        return self.title

class OfficeType(VotesmartApiObject):
    def __str__(self):
        return ': '.join((self.officeTypeId, self.name))
    
class OfficeBranch(VotesmartApiObject):
    def __str__(self):
        return ': '.join((self.officeBranchId, self.name))
    
class OfficeLevel(VotesmartApiObject):
    def __str__(self):
        return ': '.join((self.officeLevelId, self.name))
    
class Office(VotesmartApiObject):
    def __str__(self):
        return self.name
    
def _result_to_obj(cls, result):
    if isinstance(result, dict):
        return [cls(result)]
    else:
        return [cls(o) for o in result]

class votesmart(object):
    
    apikey = '496ec1875a7885ec65a4ead99579642c'
    
    @staticmethod
    def _apicall(func, params):
        if votesmart.apikey is None:
            raise VotesmartApiError('Missing Project Vote Smart apikey')
    
        params = dict([(k,v) for (k,v) in params.iteritems() if v])
        url = 'http://api.votesmart.org/%s?o=JSON&key=%s&%s' % (func,
            votesmart.apikey, urllib.urlencode(params))
        try:
            response = urllib2.urlopen(url).read()
            obj = json.loads(response)
            if 'error' in obj:
                raise VotesmartApiError(obj['error']['errorMessage'])
            else:
                return obj
        except urllib2.HTTPError, e:
            raise VotesmartApiError(e.read())
        except ValueError, e:
            raise VotesmartApiError('Invalid Response')
    
    class address(object):
        @staticmethod
        def getCampaign(candidateId):
            params = {'candidateId': candidateId}
            result = votesmart._apicall('Address.getCampaign', params)
            return [Address(o) for o in result['address']['office']]
    
        @staticmethod
        def getCampaignWebAddress(candidateId):
            params = {'candidateId': candidateId}
            result = votesmart._apicall('Address.getCampaignWebAddress', params)
            return [WebAddress(o) for o in result['webaddress']['address']]
                
        @staticmethod
        def getCampaignByElection(electionId):
            params = {'electionId': electionId}
            result = votesmart._apicall('Address.getCampaignByElection', params)
            return [Address(o) for o in result['address']['office']]
                
        @staticmethod
        def getOffice(candidateId):
            params = {'candidateId': candidateId}
            result = votesmart._apicall('Address.getOffice', params)
            return [Address(o) for o in result['address']['office']]
                
        @staticmethod
        def getOfficeWebAddress(candidateId):
            params = {'candidateId': candidateId}
            result = votesmart._apicall('Address.getOfficeWebAddress', params)
            return [WebAddress(o) for o in result['webaddress']['address']]
                
        #@staticmethod
        #def getOfficeByOfficeState(officeId, stateId=None):
        #    params = {'officeId': officeId, 'stateId': stateId}
        #    result = votesmart._apicall('Address.getOfficeByOfficeState', params)
        #    return [Address(o) for o in result['address']['office']]
            
    class candidatebio(object):
        @staticmethod
        def getBio(candidateId):
            params = {'candidateId': candidateId}
            result = votesmart._apicall('CandidateBio.getBio', params)
            return Bio(result['bio'])
            
        @staticmethod
        def getAddlBio(candidateId):
            params = {'candidateId': candidateId}
            result = votesmart._apicall('CandidateBio.getAddlBio', params)
            return [AddlBio(o) for o in result['addlbio']['additional']['item']]
            
    class candidates(object):
        @staticmethod
        def getByOfficeState(officeId, stateId=None, electionYear=None):
            params = {'officeId': officeId, 'stateId':stateId, 'electionYear': electionYear}
            result = votesmart._apicall('Candidates.getByOfficeState', params)
            return _result_to_obj(Candidate, result['candidateList']['candidate'])
                
        @staticmethod
        def getByLastname(lastName, electionYear=None):
            params = {'lastName': lastName, 'electionYear':electionYear}
            result = votesmart._apicall('Candidates.getByLastname', params)
            return _result_to_obj(Candidate, result['candidateList']['candidate'])
                
        @staticmethod
        def getByLevenstein(lastName, electionYear=None):
            params = {'lastName': lastName, 'electionYear':electionYear}
            result = votesmart._apicall('Candidates.getByLevenstein', params)
            return _result_to_obj(Candidate, result['candidateList']['candidate'])
                
        @staticmethod
        def getByElection(electionId):
            params = {'electionId': electionId}
            result = votesmart._apicall('Candidates.getByElection', params)
            return _result_to_obj(Candidate, result['candidateList']['candidate'])
                
        @staticmethod
        def getByDistrict(districtId, electionYear=None):
            params = {'districtId': districtId, 'electionYear':electionYear}
            result = votesmart._apicall('Candidates.getByDistrict', params)
            return _result_to_obj(Candidate, result['candidateList']['candidate'])
        
    class committee(object):
        @staticmethod
        def getTypes():
            result = votesmart._apicall('Committee.getTypes', {})
            return [CommitteeType(o) for o in result['committeeTypes']['type']]
            
        @staticmethod
        def getCommitteesByTypeState(typeId=None, stateId=None):
            params = {'typeId':typeId, 'stateId':stateId}
            result = votesmart._apicall('Committee.getCommitteesByTypeState', params)
            return [Committee(o) for o in result['committees']['committee']]
            
        @staticmethod
        def getCommittee(committeeId):
            params = {'committeeId' : committeeId}
            result = votesmart._apicall('Committee.getCommittee', params)
            return CommitteeDetail(result['committee'])
        
        @staticmethod
        def getCommitteeMembers(committeeId):
            params = {'committeeId' : committeeId}
            result = votesmart._apicall('Committee.getCommitteeMembers', params)
            return [CommitteeMember(o) for o in result['committeeMembers']['member']]
    
    class district(object):
        @staticmethod
        def getByOfficeState(officeId, stateId, districtName=None):
            params = {'officeId':officeId, 'stateId': stateId, 'districtName': districtName}
            result = votesmart._apicall('District.getByOfficeState', params)
            return [District(o) for o in result['districtList']['district']]
    
    class election(object):
        @staticmethod
        def getElection(electionId):
            params = {'electionId':electionId}
            result = votesmart._apicall('Election.getElection', params)
            return Election(result['elections']['election'])
            
        @staticmethod
        def getElectionByYearState(year, stateId=None):
            params = {'year':year, 'stateId':stateId}
            result = votesmart._apicall('Election.getElectionByYearState', params)
            return _result_to_obj(Election, result['elections']['election'])
            
        #@staticmethod
        #def getStageCandidates(electionId, stageId,
        #                       party=None, districtId=None, stateId=None):
        #    params = {'electionId':electionId, 'stageId':stageId, 'party':party,
        #              'districtId':districtId, 'stateId':stateId}
        #    result = votesmart._apicall('Election.getElectionByYearState', params)
        #    ['stageCandidates']['candidate']
        
    class leadership(object):
        @staticmethod
        def getPositions(stateId=None, officeId=None):
            params = {'stateId':stateId, 'officeId':officeId}
            result = votesmart._apicall('Leadership.getPositions', params)
            return [LeadershipPosition(o) for o in result['leadership']['position']]
                
        #@staticmethod
        #def getCandidates(leadershipId, stateId=None):
        #    params = {'leadershipId':leadershipId, 'stateId':stateId}
        #    result = votesmart._apicall('Leadership.getCandidates', params)
        #    return result['leaders']['leader']
            
    class local(object):
        @staticmethod
        def getCounties(stateId):
            params = {'stateId': stateId}
            result = votesmart._apicall('Local.getCounties', params)
            return [Locality(o) for o in result['counties']['county']]
            
        @staticmethod
        def getCities(stateId):
            params = {'stateId': stateId}
            result = votesmart._apicall('Local.getCities', params)
            return [Locality(o) for o in result['cities']['city']]
            
        @staticmethod
        def getOfficials(localId):
            params = {'localId': localId}
            result = votesmart._apicall('Local.getOfficials', params)
            return [Official(o) for o in result['candidateList']['candidate']]
        
    class measure(object):
        @staticmethod
        def getMeasuresByYearState(year, stateId):
            params = {'year':year, 'stateId':stateId}
            result = votesmart._apicall('Measure.getMeasuresByYearState', params)
            return _result_to_obj(Measure, result['measures']['measure'])
            
        @staticmethod
        def getMeasure(measureId):
            params = {'measureId':measureId}
            result = votesmart._apicall('Measure.getMeasure', params)
            return MeasureDetail(result['measure'])
        
    class npat(object):
        @staticmethod
        def getNpat(candidateId):
            params = {'candidateId':candidateId}
            result = votesmart._apicall('Npat.getNpat', params)
            return result['npat']
    
    class office(object):
        @staticmethod
        def getTypes():
            result = votesmart._apicall('Office.getTypes', {})
            return [OfficeType(o) for o in result['officeTypes']['type']]
        
        @staticmethod
        def getBranches():
            result = votesmart._apicall('Office.getBranches', {})
            return [OfficeBranch(o) for o in result['branches']['branch']]
    
        @staticmethod
        def getLevels():
            result = votesmart._apicall('Office.getLevels', {})
            return [OfficeLevel(o) for o in result['levels']['level']]
    
        @staticmethod
        def getOfficesByType(typeId):
            params = {'typeId':typeId}
            result = votesmart._apicall('Office.getOfficesByType', params)
            return _result_to_obj(Office, result['offices']['office'])
            
        @staticmethod
        def getOfficesByLevel(levelId):
            params = {'levelId':levelId}
            result = votesmart._apicall('Office.getOfficesByLevel', params)
            return _result_to_obj(Office, result['offices']['office'])
            
        @staticmethod
        def getOfficesByTypeLevel(typeId, levelId):
            params = {'typeId':typeId, 'levelId':levelId}
            result = votesmart._apicall('Office.getOfficesByTypeLevel', params)
            return _result_to_obj(Office, result['offices']['office'])
            
        @staticmethod
        def getOfficesByBranchLevel(branchId, levelId):
            params = {'branchId':branchId, 'levelId':levelId}
            result = votesmart._apicall('Office.getOfficesByBranchLevel', params)
            return _result_to_obj(Office, result['offices']['office'])
                
    class officials(object):
        @staticmethod
        def getByOfficeState(officeId, stateId=None):
            params = {'officeId':officeId, 'stateId': stateId}
            result = votesmart._apicall('Officials.getByOfficeState', params)
            return _result_to_obj(Official, result['candidateList']['candidate'])
                
        @staticmethod
        def getByLastname(lastName):
            params = {'lastName':lastName}
            result = votesmart._apicall('Officials.getByLastname', params)
            return _result_to_obj(Official, result['candidateList']['candidate'])
       
        @staticmethod
        def getByLevenstein(lastName):
            params = {'lastName':lastName}
            result = votesmart._apicall('Officials.getByLevenstein', params)
            return _result_to_obj(Official, result['candidateList']['candidate'])
       
        @staticmethod
        def getByElection(electionId):
            params = {'electionId':electionId}
            result = votesmart._apicall('Officials.getByElection', params)
            return _result_to_obj(Official, result['candidateList']['candidate'])
        
        @staticmethod
        def getByDistrict(districtId):
            params = {'districtId':districtId}
            result = votesmart._apicall('Officials.getByDistrict', params)
            return _result_to_obj(Official, result['candidateList']['candidate'])
    
    class rating(object):
        @staticmethod
        def getCategories(stateId=None):
            params = {'stateId':stateId}
            result = votesmart._apicall('getCategories', params)['categories']['category']
    
        @staticmethod
        def getSigList(categoryId, stateId=None):
            params = {'categoryId':categoryId, 'stateId':stateId}
            result = votesmart._apicall('getSigList', params)['sigs']['sig']
    
        @staticmethod
        def getSig(sigId):
            params = {'sigId':sigId}
            result = votesmart._apicall('getSig', params)['sig']
    
        @staticmethod
        def getCandidateRating(candidateId, sigId):
            params = {'candidateId':candidateId, 'sigId':sigId}
            result = votesmart._apicall('getCandidateRating', params)['candidateRating']['rating']
    
    class state(object):
        @staticmethod
        def getStateIDs(self):
            result = votesmart._apicall('getStateIDs', {})['stateList']['list']['state']
    
        @staticmethod
        def getState(stateId):
            params = {'stateId':stateId}
            result = votesmart._apicall('getState', params)['state']['details']
                
    class votes(object):
        @staticmethod
        def getCategories(year, stateId=None):
            params = {'year':year, 'stateId':stateId}
            result = votesmart._apicall('getCategories', params)['categories']['category']
            
        @staticmethod
        def getBill(billId):
            params = {'billId':billId}
            result = votesmart._apicall('getBill', params)['bill']
        
        @staticmethod
        def getBillAction(actionId):
            params = {'actionId':actionId}
            result = votesmart._apicall('getBillAction', params)['action']
        
        @staticmethod
        def getBillActionVotes(actionId):
            params = {'actionId':actionId}
            result = votesmart._apicall('getBillActionVotes', params)['votes']['vote']
        
        @staticmethod
        def getBillActionVoteByOfficial(actionId, candidateId):
            params = {'actionId':actionId, 'candidateId':candidateId}
            result = votesmart._apicall('getBillActionVoteByOfficial', params)['bills']['bill']
            
        @staticmethod
        def getBillsByCategoryYearState(categoryId, year, stateId=None):
            params = {'categoryId':categoryId, 'year':year, 'stateId':stateId}
            result = votesmart._apicall('getBillsByCategoryYearState', params)['bills']['bill']
            
        @staticmethod
        def getBillsByYearState(year, stateId=None):
            params = {'year':year, 'stateId':stateId}
            result = votesmart._apicall('getBillsByYearState', params)['bills']['bill']
            
        @staticmethod
        def getBillsByOfficialYearOffice(candidateId, year, officeId=None):
            params = {'candidateId':candidateId, 'year':year, 'officeId':officeId}
            result = votesmart._apicall('getBillsByOfficialYearOffice', params)['bills']['bill']
            
        @staticmethod
        def getBillsByCandidateCategoryOffice(candidateId, categoryId, officeId=None):
            params = {'candidateId':candidateId, 'categoryId':categoryId, 'officeId':officeId}
            result = votesmart._apicall('getBillsByCandidateCategoryOffice', params)['bills']['bill']
            
        @staticmethod
        def getBillsBySponsorYear(candidateId, year):
            params = {'candidateId':candidateId, 'year':year}
            result = votesmart._apicall('getBillsBySponsorYear', params)['bills']['bill']
            
        @staticmethod
        def getBillsBySponsorCategory(candidateId, categoryId):
            params = {'candidateId':candidateId, 'categoryId':categoryId}
            result = votesmart._apicall('getBillsBySponsorCategory', params)['bills']['bill']
        
        @staticmethod    
        def getBillsByStateRecent(stateId=None, amount=None):
            params = {'stateId':stateId, 'amount':amount}
            result = votesmart._apicall('getBillsByStateRecent', params)['bills']['bill']
                
        @staticmethod
        def getVetoes(candidateId):
            params = {'candidateId': candidateId}
            result = votesmart._apicall('getVetoes', params)['vetoes']['veto']