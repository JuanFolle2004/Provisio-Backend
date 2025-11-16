<?php

declare(strict_types=1);

namespace Src\Groups\App\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;
use Src\Groups\Domain\Model\Message;

/** @mixin Message */
class MessageResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'author' => $this->user->username,
            'content' => $this->content,
            'time' => $this->created_at,
        ];
    }
}
