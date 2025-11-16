<?php
declare(strict_types=1);
namespace Src\Groups\App\Controllers;

use Illuminate\Container\Attributes\CurrentUser;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\Log;
use Src\Groups\App\Requests\WriteMessageRequest;
use Src\Groups\App\Resources\MessageResource;
use Src\Groups\Domain\MessageSentEvent;
use Src\Groups\Domain\Model\Message;
use Src\Groups\Domain\Model\Thread;

class PostMessageController
{
  public function __invoke(#[CurrentUser] $user, WriteMessageRequest $request):JsonResponse
  {
      $dto = $request->toDto();
      $thread = $dto->group->thread;
      if (!$thread) {
          $dto->group->thread()->save(new Thread());
      }

      $message = $thread->messages()->create([
          'content'  => $dto->content,
          'user_id'  => $user->id,
      ]);

      Log::info("Broadcasting on channel: ");
      broadcast(new MessageSentEvent($dto->group,$message))->toOthers();
      return MessageResource::make($message)->response();
  }
}
