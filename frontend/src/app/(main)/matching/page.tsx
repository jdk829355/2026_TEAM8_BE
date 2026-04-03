"use client"

import { Input } from "@/components/ui/input"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Heart, MessageSquare, Search } from "lucide-react"
import { useAnnouncements } from "@/hooks/useQueries"
import api from "@/lib/api"
import { useRouter } from "next/navigation"
import { useState } from "react"

export default function MatchingPage() {
  const router = useRouter()
  const { data: announcements, isLoading } = useAnnouncements()
  const [creating, setCreating] = useState<string | null>(null)

  const handleSendMessage = async (announcementId: string, announcerName: string) => {
    try {
      setCreating(announcementId)
      const { data } = await api.post('/chat/room', { 
        announcement_id: announcementId, 
        name: `${announcerName}님과의 채팅` 
      })
      router.push(`/messages/${data.room_id}`)
    } catch (e) {
      console.error(e)
      alert('채팅방 생성에 실패했습니다.')
    } finally {
      setCreating(null)
    }
  }

  const matches = Array.isArray(announcements) ? announcements : []

  return (
    <div className="space-y-6 pb-10">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">매칭 찾기</h1>
        <p className="text-slate-600">나와 재능을 교환할 메이트를 찾아보세요</p>
      </div>

      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 w-5 h-5" />
        <Input 
          className="pl-10 h-12 bg-slate-50 border-slate-200 rounded-xl"
          placeholder="배우고 싶은 재능을 검색해보세요..." 
        />
      </div>

      <Tabs defaultValue="recommended" className="w-full">
        <TabsList className="grid w-full grid-cols-3 h-12 bg-slate-100 rounded-xl p-1 mb-6">
          <TabsTrigger value="recommended" className="rounded-lg data-[state=active]:bg-white data-[state=active]:shadow-sm">최신 공고</TabsTrigger>
          <TabsTrigger value="teach" className="rounded-lg data-[state=active]:bg-white data-[state=active]:shadow-sm">가르칠 재능</TabsTrigger>
          <TabsTrigger value="learn" className="rounded-lg data-[state=active]:bg-white data-[state=active]:shadow-sm">배우고 싶은 재능</TabsTrigger>
        </TabsList>
        
        <TabsContent value="recommended" className="space-y-4 outline-none">
          {isLoading ? (
             <div className="text-center py-10 text-slate-500">공고를 불러오는 중...</div>
          ) : matches.length === 0 ? (
             <div className="text-center py-10 text-slate-500">등록된 공고가 없습니다.</div>
          ) : (
            matches.map((match: any) => (
              <Card key={match.id} className="border-slate-100 shadow-sm overflow-hidden hover:shadow-md transition-shadow">
                <CardContent className="p-6">
                  <div className="flex justify-between">
                    <div className="flex gap-4">
                      <Avatar className="w-16 h-16">
                        <AvatarFallback className="text-lg bg-blue-100 text-blue-600 font-bold">{match.username?.[0] || "?"}</AvatarFallback>
                      </Avatar>
                      
                      <div className="space-y-2 flex flex-col justify-center">
                        <div className="flex items-center gap-2">
                          <span className="text-lg font-bold">{match.username}</span>
                        </div>
                        
                        <div className="text-sm space-y-1 text-slate-700">
                          <div><span className="text-slate-500 mr-2">가르칠 수 있어요:</span>{match.can_teach_skill}</div>
                          <div><span className="text-slate-500 mr-2">배우고 싶어요:</span>{match.want_to_skill}</div>
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex gap-2 items-start mt-2">
                      <Button variant="outline" size="icon" className="text-slate-400 hover:text-red-500 rounded-full w-10 h-10">
                        <Heart className="w-5 h-5" />
                      </Button>
                      <Button 
                        onClick={() => handleSendMessage(match.id, match.username)}
                        disabled={creating === match.id}
                        className="bg-yellow-400 hover:bg-yellow-500 text-yellow-950 font-bold gap-2 pl-4 pr-5 rounded-full"
                      >
                        <MessageSquare className="w-4 h-4 fill-current" /> 
                        {creating === match.id ? "생성 중..." : "메시지 보내기"}
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </TabsContent>
        {/* Fill others with dummy empty state or identical list for now */}
        <TabsContent value="teach">
           <div className="text-center py-10 text-slate-500">가르칠 수 있는 재능 목록이 표시됩니다.</div>
        </TabsContent>
        <TabsContent value="learn">
           <div className="text-center py-10 text-slate-500">배우고 싶은 재능 목록이 표시됩니다.</div>
        </TabsContent>
      </Tabs>
    </div>
  )
}
