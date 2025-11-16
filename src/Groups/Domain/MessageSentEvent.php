<?php
declare(strict_types=1);
namespace Src\Groups\Domain;

use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Contracts\Broadcasting\ShouldBroadcastNow;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;
use Src\Groups\Domain\Model\Group;
use Src\Groups\Domain\Model\Message;

class MessageSentEvent implements ShouldBroadcast
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    public function __construct(
        public readonly Group $group,
        public readonly Message $message
    )
    {
        \Log::info('Broadcasting message', [
            'group_id' => $group->id,
            'message_id' => $message->id,
            'channel' => 'chat.group.' . $group->id
        ]);
    }

    public function broadcastOn(): array
    {
        $channel = 'chat.group.' . $this->group->id;
        \Log::info('Broadcasting on channel: ' . $channel);
        return [
            new PrivateChannel('chat.group.' . $this->group->id),
        ];
    }

    public function broadcastAs(): string
    {
        return 'MessageSentEvent';
    }

    public function broadcastWith(): array
    {
        \Log::info('Broadcasting payload made');
        return [
            'id' => $this->message->id,
            'author' => $this->message->user->username,
            'content' => $this->message->content,
            'time' => $this->message->created_at,];
    }
}
